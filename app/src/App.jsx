import { prepareMessages, retryLatestUser } from "./messages.mjs";
import React, { useState, useEffect, useMemo, useRef } from "react";
import {
  AssistantRuntimeProvider,
  useLocalRuntime,
  ThreadPrimitive,
  MessagePrimitive,
  ComposerPrimitive,
} from "@assistant-ui/react";
import { MarkdownTextPrimitive } from "@assistant-ui/react-markdown";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
const markdownPlugins = [remarkGfm];
function MarkdownText() {
  return <MarkdownTextPrimitive remarkPlugins={markdownPlugins} />;
}
import {
  ArrowUpRight,
  ArrowRight,
  Plus,
  Focus,
  MessagesSquare,
  FlaskConical,
  Command,
  ChevronRight,
  Check,
  LockKeyhole,
  RefreshCw,
  Download,
  ArrowUp,
  Square,
  Clock3,
  PanelLeftClose,
  Sparkles,
  FileText,
  AlertCircle,
  Trash2,
  CheckCircle2,
} from "lucide-react";

const TASKS = [
  {
    id: "frame",
    title: "釐清需求",
    english: "FRAME THE PROBLEM",
    number: "01",
    technique: "#44",
    icon: Focus,
    description: "把模糊的需求，拆成值得先解的問題。",
    deliverable: "一份範圍清楚的問題定義",
    tags: ["問題切片", "優先順序", "下一步"],
    sample: {
      decision: "客戶想導入客服 AI，第一個試點應該從哪個流程開始？",
      evidence:
        "客服每天需要查找產品規格。文件有版本，但尚未測量查找耗時與錯誤率。",
      constraints: "兩週、兩位工程師。只能使用去識別化範例，先不串接正式系統。",
    },
  },
  {
    id: "critique",
    title: "提案預演",
    english: "CHALLENGE THE IDEA",
    number: "02",
    technique: "#31",
    icon: MessagesSquare,
    description: "預演決策者的追問，找出證據缺口。",
    deliverable: "一份提案追問與補證據清單",
    tags: ["角色模擬", "證據缺口", "會前準備"],
    sample: {
      decision: "是否核准為期四週的內部知識查詢 AI 試點？",
      evidence:
        "已有可操作 Demo，五位同事試用後反應正面；尚未測量正確率、總處理時間或成本。",
      constraints:
        "預算五萬元，由財務、資訊、營運主管共同決策。資料不能傳到未核准的外部系統。",
    },
  },
  {
    id: "validate",
    title: "設計驗證",
    english: "TEST THE ASSUMPTION",
    number: "03",
    technique: "#37",
    icon: FlaskConical,
    description: "把「應該有用」，變成能驗證的假設。",
    deliverable: "一份可執行的最小驗證計畫",
    tags: ["比較基準", "觀察指標", "停止條件"],
    sample: {
      decision: "AI 摘要是否能降低顧問閱讀訪談紀錄的總耗時？",
      evidence:
        "有十份經同意且已去識別化的訪談紀錄，尚無耗時與摘要品質的基準。",
      constraints:
        "一週、三位顧問。需將人工核對時間納入，先協議品質門檻再測試。",
    },
  },
];
const EMPTY = { decision: "", evidence: "", constraints: "" };
const HISTORY_KEY = "thinking-os.history.v1";
function readHistory() {
  try {
    const v = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
    return Array.isArray(v)
      ? v
          .filter(
            (x) =>
              x &&
              TASKS.some((t) => t.id === x.task) &&
              typeof x.text === "string" &&
              x.brief,
          )
          .slice(0, 20)
      : [];
  } catch {
    return [];
  }
}
function exportMarkdown(item) {
  const task = TASKS.find((t) => t.id === item.task);
  const content =
    "# " +
    task.title +
    "：" +
    item.brief.decision +
    "\n\n> 引擎：" +
    item.provider +
    " · " +
    new Date(item.date).toLocaleString("zh-TW") +
    "\n\n## 決策情境\n\n" +
    item.brief.decision +
    "\n\n### 已知資訊\n" +
    item.brief.evidence +
    "\n\n### 限制\n" +
    item.brief.constraints +
    "\n\n---\n\n" +
    item.text;
  const url = URL.createObjectURL(
    new Blob([content], { type: "text/markdown;charset=utf-8" }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download =
    "thinking-" +
    item.task +
    "-" +
    new Date(item.date).toISOString().slice(0, 10) +
    ".md";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function Mark() {
  return (
    <span className="brand-mark">
      <span />
      <span />
      <span />
    </span>
  );
}
function UserMessage() {
  return (
    <MessagePrimitive.Root className="user-message">
      <span className="message-label">你的補充</span>
      <MessagePrimitive.Parts />
    </MessagePrimitive.Root>
  );
}
function AssistantMessage() {
  return (
    <MessagePrimitive.Root className="assistant-message">
      <div className="author">
        <Mark />
        <span>Thinking partner</span>
        <span className="tiny-tag">分析草稿</span>
      </div>
      <div className="markdown">
        <MessagePrimitive.Parts components={{ Text: MarkdownText }} />
      </div>
      <MessagePrimitive.Error>
        <div className="inline-error">本次未完成，請查看上方訊息後重試。</div>
      </MessagePrimitive.Error>
    </MessagePrimitive.Root>
  );
}

function Conversation({ session, token, onSave, onBusy, onLatest }) {
  const [error, setError] = useState(""),
    [status, setStatus] = useState("");
  const callbacks = useRef({ onSave, onBusy, onLatest });
  callbacks.current = { onSave, onBusy, onLatest };
  const adapter = useMemo(
    () => ({
      async *run({ messages, abortSignal }) {
        setError("");
        setStatus("正在連接本機引擎…");
        callbacks.current.onBusy(true);
        let text = "",
          done = false,
          reader;
        try {
          const response = await fetch("/api/run", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-Session-Token": token,
            },
            body: JSON.stringify({
              ...session,
              messages: prepareMessages(messages),
            }),
            signal: abortSignal,
          });
          if (!response.ok) {
            const body = await response.json();
            throw new Error(body.error || "無法啟動分析。");
          }
          reader = response.body.getReader();
          const decoder = new TextDecoder();
          let buffer = "";
          while (true) {
            const chunk = await reader.read();
            buffer += decoder.decode(chunk.value || new Uint8Array(), {
              stream: !chunk.done,
            });
            const lines = buffer.split("\n");
            buffer = lines.pop() || "";
            if (chunk.done && buffer.trim()) lines.push(buffer);
            for (const line of lines) {
              if (!line.trim()) continue;
              const event = JSON.parse(line);
              if (event.type === "error") throw new Error(event.message);
              if (event.type === "status") setStatus(event.message);
              if (event.type === "text") {
                text =
                  event.mode === "replace" ? event.text : text + event.text;
                setStatus("正在整理分析…");
                yield { content: [{ type: "text", text }] };
              }
              if (event.type === "done") done = true;
            }
            if (chunk.done) break;
          }
          if (!done || !text)
            throw new Error("連線在分析完成前中斷，請重新執行。");
          const result = { ...session, text, date: new Date().toISOString() };
          callbacks.current.onSave(result);
          callbacks.current.onLatest(result);
          setStatus("已完成 · 結果已存於這個瀏覽器");
        } catch (e) {
          if (abortSignal.aborted) {
            setStatus("已停止 · 未完成的回覆不會存入成果紀錄");
          } else {
            setError(e.message);
            setStatus("本次未完成");
            throw e;
          }
        } finally {
          reader?.releaseLock();
          callbacks.current.onBusy(false);
        }
      },
    }),
    [session, token],
  );
  const runtime = useLocalRuntime(adapter);
  const started = useRef(false);
  useEffect(() => {
    if (!started.current) {
      started.current = true;
      runtime.thread.append("請依已填寫的決策、已知資訊與限制，開始本次分析。");
    }
    return () => runtime.thread.cancelRun();
  }, [runtime]);
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <ThreadPrimitive.Root className="thread">
        {error && (
          <div role="alert" className="error-banner">
            <AlertCircle size={18} />
            <div>
              <strong>需要處理後再繼續</strong>
              <p>{error}</p>
              <button
                className="text-button"
                onClick={() => retryLatestUser(runtime.thread)}
              >
                重試本次分析 <ArrowRight size={14} />
              </button>
            </div>
          </div>
        )}
        <ThreadPrimitive.Viewport className="thread-viewport">
          <ThreadPrimitive.Messages
            components={{ UserMessage, AssistantMessage }}
          />
          <ThreadPrimitive.If running>
            <div className="thinking">
              <span />
              <span />
              <span />
              正在思考這個決策
            </div>
          </ThreadPrimitive.If>
        </ThreadPrimitive.Viewport>
        <div className="composer-wrap">
          <ComposerPrimitive.Root className="composer">
            <ComposerPrimitive.Input
              placeholder="補充背景，或針對這個決策追問…"
              aria-label="補充背景或追問"
              rows={2}
            />
            <ThreadPrimitive.If running={false}>
              <ComposerPrimitive.Send
                className="send-button"
                aria-label="送出補充"
              >
                <ArrowUp size={20} />
              </ComposerPrimitive.Send>
            </ThreadPrimitive.If>
            <ThreadPrimitive.If running>
              <ComposerPrimitive.Cancel
                className="send-button stop"
                aria-label="停止分析"
              >
                <Square size={16} />
              </ComposerPrimitive.Cancel>
            </ThreadPrimitive.If>
          </ComposerPrimitive.Root>
          <div className="stream-status" aria-live="polite">
            {status || "補充問題會沿用本次任務與情境。"}
          </div>
        </div>
      </ThreadPrimitive.Root>
    </AssistantRuntimeProvider>
  );
}

export default function App() {
  const [taskId, setTaskId] = useState("frame"),
    [brief, setBrief] = useState({ ...EMPTY }),
    [provider, setProvider] = useState("codex");
  const [boot, setBoot] = useState(null),
    [checking, setChecking] = useState(true),
    [connectionError, setConnectionError] = useState("");
  const [session, setSession] = useState(null),
    [busy, setBusy] = useState(false),
    [latest, setLatest] = useState(null),
    [archive, setArchive] = useState(null);
  const [history, setHistory] = useState(readHistory),
    [storageError, setStorageError] = useState(""),
    [mobileNav, setMobileNav] = useState(false);
  const task = TASKS.find((t) => t.id === taskId),
    Icon = task.icon;
  async function refresh() {
    setChecking(true);
    setConnectionError("");
    try {
      const r = await fetch("/api/bootstrap");
      if (!r.ok) throw new Error("無法連上本機服務。");
      setBoot(await r.json());
    } catch (e) {
      setConnectionError(e.message);
    } finally {
      setChecking(false);
    }
  }
  useEffect(() => {
    refresh();
  }, []);
  function save(item) {
    setHistory((previous) => {
      const next = [item, ...previous.filter((p) => p.id !== item.id)].slice(
        0,
        20,
      );
      try {
        localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
        setStorageError("");
      } catch {
        setStorageError("瀏覽器儲存空間不足，請先下載成果。");
      }
      return next;
    });
  }
  function reset(id = taskId) {
    if (busy) return;
    setSession(null);
    setArchive(null);
    setLatest(null);
    setTaskId(id);
    setMobileNav(false);
  }
  function start(e) {
    e.preventDefault();
    if (!boot?.providers[provider]?.ready) return;
    setArchive(null);
    setLatest(null);
    setSession({
      id: crypto.randomUUID(),
      task: taskId,
      provider,
      brief: { ...brief },
    });
  }
  const selectedStatus = boot?.providers[provider];
  const completed = Object.values(brief).filter(
    (v) => v.trim().length >= 3,
  ).length;
  return (
    <div className="app-shell">
      {mobileNav && (
        <button
          className="mobile-backdrop"
          aria-label="關閉導覽"
          onClick={() => setMobileNav(false)}
        />
      )}
      <aside className={"sidebar " + (mobileNav ? "open" : "")}>
        <a className="brand" href="/" aria-label="AI Thinking OS 首頁">
          <Mark />
          <span>
            Thinking OS<small>YOUR DECISION WORKSPACE</small>
          </span>
        </a>
        <button
          className="new-session"
          disabled={busy}
          onClick={() => {
            reset();
            setBrief({ ...EMPTY });
          }}
        >
          <Plus size={18} />
          新的思考工作階段<span>↗</span>
        </button>
        <p className="nav-label">
          工作台 <span>03</span>
        </p>
        <nav>
          {TASKS.map((t) => (
            <button
              key={t.id}
              disabled={busy}
              className={"nav-item " + (taskId === t.id ? "active" : "")}
              onClick={() => reset(t.id)}
            >
              <t.icon size={19} />
              <span>{t.title}</span>
              <span className="nav-number">{t.number}</span>
            </button>
          ))}
        </nav>
        <div className="history-heading">
          <p className="nav-label">最近的成果</p>
          <span>{history.length}</span>
        </div>
        <div className="history-list">
          {history.length ? (
            history.map((item) => (
              <button
                className={
                  "history-item " + (archive?.id === item.id ? "selected" : "")
                }
                disabled={busy}
                key={item.id}
                onClick={() => {
                  setArchive(item);
                  setTaskId(item.task);
                  setSession(null);
                  setLatest(null);
                  setMobileNav(false);
                }}
              >
                <FileText size={15} />
                <span>
                  {item.brief.decision}
                  <small>
                    {new Date(item.date).toLocaleDateString("zh-TW", {
                      month: "2-digit",
                      day: "2-digit",
                    })}{" "}
                    · {TASKS.find((t) => t.id === item.task)?.title}
                  </small>
                </span>
              </button>
            ))
          ) : (
            <div className="history-empty">
              <Clock3 size={18} />
              <p>
                好決策，值得留下。
                <br />
                完成的分析會出現在這裡。
              </p>
            </div>
          )}
        </div>
        <div className="sidebar-bottom">
          <div className="local-mode">
            <span className="status-dot" />
            <span>個人本機版</span>
            <span className="version">v0.1</span>
          </div>
          <p>
            成果留在這個瀏覽器
            <br />
            使用你自己的 AI 訂閱
          </p>
          {history.length > 0 && (
            <button
              className="text-button subtle"
              onClick={() => {
                localStorage.removeItem(HISTORY_KEY);
                setHistory([]);
                setArchive(null);
              }}
            >
              <Trash2 size={13} />
              清除本機成果紀錄
            </button>
          )}
        </div>
      </aside>
      <main className="main">
        <header className="topbar">
          <div className="breadcrumbs">
            <button
              className="mobile-toggle"
              aria-label="開啟導覽"
              onClick={() => setMobileNav(!mobileNav)}
            >
              <PanelLeftClose size={20} />
            </button>
            <span>工作台</span>
            <ChevronRight size={14} />
            <strong>{task.title}</strong>
          </div>
          <div className="private-badge">
            <LockKeyhole size={13} />
            私人工作空間
          </div>
        </header>
        <div className="workspace">
          <div className="page-heading">
            <div className="eyebrow">
              <span />
              THINK CLEARER. DECIDE BETTER.
            </div>
            <div className="heading-row">
              <h1>
                {session || archive ? (
                  task.title + "工作階段"
                ) : (
                  <>
                    先把問題想清楚，
                    <br className="small-break" />
                    再決定下一步。
                  </>
                )}
              </h1>
              <span className="edition">
                PERSONAL
                <br />
                WORKSPACE / 01
              </span>
            </div>
            <p>
              {session || archive
                ? "帶著清楚的範圍，推進這一個決策。"
                : "選一個你現在需要的成果。讓 AI 陪你拆解，而你保留判斷。"}
            </p>
          </div>
          {!session && !archive && (
            <div className="task-grid">
              {TASKS.map((t) => (
                <button
                  key={t.id}
                  className={"task-card " + (taskId === t.id ? "selected" : "")}
                  onClick={() => setTaskId(t.id)}
                >
                  <div className="card-top">
                    <t.icon size={23} />
                    <span>{t.number}</span>
                  </div>
                  <div className="task-title">
                    {t.title}
                    {taskId === t.id ? (
                      <CheckCircle2 size={18} />
                    ) : (
                      <ArrowUpRight size={18} />
                    )}
                  </div>
                  <p>{t.description}</p>
                  <span className="technique">
                    {t.technique}
                    <span className="technique-description">
                      {" "}
                      · {t.english}
                    </span>
                  </span>
                </button>
              ))}
            </div>
          )}
          <div className="work-grid">
            <section className="work-panel">
              <div className="panel-header">
                <div>
                  <span className="section-index">
                    {session || archive ? "02" : "01"}
                  </span>
                  <h2>
                    {archive
                      ? "已儲存的成果"
                      : session
                        ? "一起推進這個問題"
                        : "定義這次的思考邊界"}
                  </h2>
                </div>
                {latest || archive ? (
                  <button
                    className="secondary-button"
                    onClick={() => exportMarkdown(archive || latest)}
                  >
                    <Download size={15} />
                    下載 Markdown
                  </button>
                ) : (
                  <span className="completion">{completed}/3 已填寫</span>
                )}
              </div>
              {storageError && (
                <div role="alert" className="error-banner">
                  {storageError}
                </div>
              )}
              {archive ? (
                <div className="archive">
                  <div className="archive-meta">
                    <CheckCircle2 size={16} />
                    完成於 {new Date(archive.date).toLocaleString(
                      "zh-TW",
                    )} · {archive.provider}
                  </div>
                  <h2>{archive.brief.decision}</h2>
                  <div className="archive-text markdown">
                    <ReactMarkdown remarkPlugins={markdownPlugins}>
                      {archive.text}
                    </ReactMarkdown>
                  </div>
                  <button
                    className="secondary-button"
                    onClick={() => {
                      setBrief(archive.brief);
                      reset(archive.task);
                    }}
                  >
                    以這份情境開始新分析 <ArrowRight size={15} />
                  </button>
                </div>
              ) : session ? (
                <Conversation
                  key={session.id}
                  session={session}
                  token={boot.token}
                  onSave={save}
                  onBusy={setBusy}
                  onLatest={setLatest}
                />
              ) : (
                <form onSubmit={start} className="brief-form">
                  <div className="form-intro">
                    <p>好的分析，從具體的情境開始。</p>
                    <button
                      type="button"
                      className="text-button"
                      onClick={() => setBrief({ ...task.sample })}
                    >
                      帶入範例 <ArrowUpRight size={14} />
                    </button>
                  </div>
                  <label className="field">
                    <span>
                      <b>你要做出什麼決策？</b>
                      <em>必填</em>
                    </span>
                    <textarea
                      required
                      minLength={3}
                      maxLength={6000}
                      rows={2}
                      value={brief.decision}
                      onChange={(e) =>
                        setBrief({ ...brief, decision: e.target.value })
                      }
                      placeholder={task.sample.decision}
                    />
                    <small>描述需要決定的事，讓這次分析有明確的終點。</small>
                  </label>
                  <label className="field">
                    <span>
                      <b>目前已知什麼？</b>
                      <em>必填</em>
                    </span>
                    <textarea
                      required
                      minLength={3}
                      maxLength={6000}
                      rows={3}
                      value={brief.evidence}
                      onChange={(e) =>
                        setBrief({ ...brief, evidence: e.target.value })
                      }
                      placeholder="貼上現有資料、觀察或提案。還沒有數據，也可以直接說明。"
                    />
                    <small>可提供實際觀察；尚未確認的資訊請標示為假設。</small>
                  </label>
                  <label className="field">
                    <span>
                      <b>這次有哪些限制？</b>
                      <em>必填</em>
                    </span>
                    <textarea
                      required
                      minLength={3}
                      maxLength={6000}
                      rows={2}
                      value={brief.constraints}
                      onChange={(e) =>
                        setBrief({ ...brief, constraints: e.target.value })
                      }
                      placeholder="例如：兩週、兩位工程師，先不串接正式系統。"
                    />
                    <small>時間、人力、預算，以及不能跨過的範圍。</small>
                  </label>
                  <div className="form-footer">
                    <span>
                      <LockKeyhole size={14} />
                      情境將送至選定的模型服務
                    </span>
                    <button
                      className="primary-button"
                      disabled={
                        completed < 3 || checking || !selectedStatus?.ready
                      }
                    >
                      開始{task.title}
                      <ArrowRight size={17} />
                    </button>
                  </div>
                </form>
              )}
            </section>
            <aside className="context-column">
              <section className="outcome-card">
                <div className="outcome-label">
                  <Sparkles size={15} />
                  這次帶走的成果
                </div>
                <Icon size={31} strokeWidth={1.5} />
                <h3>{task.deliverable}</h3>
                <div className="tag-row">
                  {task.tags.map((tag) => (
                    <span key={tag}>{tag}</span>
                  ))}
                </div>
                <div className="scope-list">
                  <div>
                    <Check size={15} />
                    <span>一次聚焦一個決策</span>
                  </div>
                  <div>
                    <Check size={15} />
                    <span>分清事實、假設與未知</span>
                  </div>
                  <div>
                    <Check size={15} />
                    <span>足夠推進，就完成這一步</span>
                  </div>
                </div>
                <p className="scope-note">
                  本次只做分析與建議。
                  <br />
                  需要研究、實作或發布時，另開任務。
                </p>
              </section>
              <section className="engine-card">
                <div className="engine-heading">
                  <h3>你的思考引擎</h3>
                  <button
                    aria-label="重新檢查引擎"
                    title="重新檢查登入狀態"
                    className={"icon-button " + (checking ? "spin" : "")}
                    onClick={refresh}
                    disabled={checking || busy}
                  >
                    <RefreshCw size={15} />
                  </button>
                </div>
                <p>透過本機 CLI 使用既有訂閱</p>
                <div className="engine-options">
                  {["codex", "claude"].map((p) => (
                    <button
                      key={p}
                      disabled={!!session || busy}
                      onClick={() => setProvider(p)}
                      className={
                        "engine-option " + (provider === p ? "selected" : "")
                      }
                    >
                      <span className="engine-symbol">
                        {p === "codex" ? <Command size={17} /> : <span>✳</span>}
                      </span>
                      <span>
                        <strong>
                          {p === "codex" ? "Codex" : "Claude Code"}
                        </strong>
                        <small
                          className={
                            boot?.providers[p]?.ready ? "ready" : "pending"
                          }
                        >
                          {checking
                            ? "檢查登入中…"
                            : boot?.providers[p]?.label || "尚未連線"}
                        </small>
                      </span>
                      <span className="radio-mark" />
                    </button>
                  ))}
                </div>
                {connectionError && (
                  <p role="alert" className="engine-error">
                    {connectionError}
                  </p>
                )}
                {!checking && !selectedStatus?.ready && (
                  <div className="login-help">
                    在終端完成登入後，按上方重新檢查。
                    <code>
                      {provider === "codex"
                        ? "codex login"
                        : "claude auth login"}
                    </code>
                  </div>
                )}
                <div className="engine-foot">
                  <LockKeyhole size={12} />
                  登入憑證由你的 CLI 管理
                </div>
              </section>
              {(session || archive) && (
                <section className="brief-summary">
                  <h3>本次情境</h3>
                  {Object.entries({
                    decision: "決策",
                    evidence: "已知",
                    constraints: "限制",
                  }).map(([key, label]) => (
                    <div key={key}>
                      <strong>{label}</strong>
                      <p>{(archive || session).brief[key]}</p>
                    </div>
                  ))}
                  <button
                    className="text-button"
                    disabled={busy}
                    onClick={() => {
                      setBrief((archive || session).brief);
                      reset();
                    }}
                  >
                    調整邊界，另開分析 <ArrowRight size={14} />
                  </button>
                </section>
              )}
              <p className="footnote">
                56 個思考技法，按需選用。
                <br />
                第一版先專注最常見的三種決策。
              </p>
            </aside>
          </div>
          <footer className="page-footer">
            <span>AI THINKING OS</span>
            <span>把好問題，變成好決策。</span>
            <span>BUILT FOR THOUGHTFUL WORK</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
