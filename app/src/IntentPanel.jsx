import React, { useState, useRef, useEffect } from "react";
const names = { frame: "釐清需求", critique: "提案預演", validate: "設計驗證" };
export default function IntentPanel({
  token,
  configured,
  enabled,
  onEnabled,
  onConfigured,
  onSelect,
}) {
  const [text, setText] = useState(""),
    [key, setKey] = useState(""),
    [working, setWorking] = useState(false),
    [result, setResult] = useState(null),
    [notice, setNotice] = useState("");
  const controller = useRef(null);
  useEffect(() => () => controller.current?.abort(), []);
  async function post(path, payload) {
    controller.current?.abort();
    controller.current = new AbortController();
    const response = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Session-Token": token },
      body: JSON.stringify(payload),
      signal: controller.current.signal,
    });
    const value = await response.json();
    if (!response.ok) throw new Error(value.error || "請求未完成。");
    return value;
  }
  async function configure(clear = false) {
    setWorking(true);
    setNotice("");
    setResult(null);
    const supplied = clear ? "" : key.trim();
    setKey("");
    try {
      const value = await post("/api/intent/settings", { apiKey: supplied });
      onConfigured(value.configured);
      onEnabled(value.configured);
      setNotice(
        value.configured
          ? "金鑰已暫存在本機服務；第一次判斷時會驗證是否可用。"
          : "已清除本機服務中的金鑰。",
      );
    } catch (e) {
      if (e.name !== "AbortError") setNotice(e.message);
    } finally {
      setWorking(false);
    }
  }
  async function suggest(e) {
    e.preventDefault();
    setWorking(true);
    setNotice("");
    setResult(null);
    try {
      setResult(await post("/api/intent", { message: text }));
    } catch (e) {
      if (e.name !== "AbortError") setNotice(e.message);
    } finally {
      setWorking(false);
    }
  }
  return (
    <section className="intent-panel" aria-label="意圖選招">
      <div className="intent-heading">
        <div>
          <span className="eyebrow">START WITH YOUR QUESTION</span>
          <h2>不知道選哪一招？先說你想解決什麼。</h2>
        </div>
        <span className="tiny-tag">
          {configured ? "Jev 已設定" : "可手動選招"}
        </span>
      </div>
      <form onSubmit={suggest} className="intent-form">
        <label className="field">
          <span>這次想完成的事</span>
          <textarea
            aria-label="想解決的問題"
            value={text}
            disabled={working}
            maxLength={24000}
            minLength={3}
            required
            rows={2}
            onChange={(e) => {
              setText(e.target.value);
              setResult(null);
            }}
            placeholder="例如：明天要提案，幫我預演主管可能問什麼。也可輸入 #31 加上問題。"
          />
        </label>
        <button
          className="secondary-button"
          disabled={!token || working || text.trim().length < 3}
        >
          {working ? "處理中…" : "建議一個任務"}
        </button>
      </form>
      {result && (
        <div className="intent-result" role="status">
          <p>{result.message}</p>
          {names[result.task] && (
            <button
              className="primary-button"
              onClick={() => {
                onSelect(result.task, text);
                setResult(null);
              }}
            >
              套用「{names[result.task]}」
            </button>
          )}
        </div>
      )}
      <details className="intent-settings">
        <summary>連接自己的 Jev（選用）</summary>
        <p>
          Jev 負責選招，分析仍由 Codex／Claude Code 完成。需另備 TypeSafe API
          key；Jev 用量由 TypeSafe 帳號計算。
        </p>
        <p>
          點選建議或開啟逐輪判斷後，文字會送至
          TypeSafe。金鑰送到本機服務後只保存在記憶體，不存入瀏覽器紀錄；服務重啟後需重新輸入。
        </p>
        <form
          className="intent-key-form"
          onSubmit={(e) => {
            e.preventDefault();
            configure();
          }}
        >
          <label className="field">
            <span>TypeSafe API key</span>
            <input
              type="password"
              autoComplete="off"
              spellCheck={false}
              aria-label="TypeSafe API key"
              value={key}
              maxLength={512}
              onChange={(e) => setKey(e.target.value)}
              disabled={working}
              placeholder="只送至本機後端"
            />
          </label>
          <button
            className="secondary-button"
            disabled={!token || working || !key.trim()}
          >
            暫存金鑰
          </button>
          {configured && (
            <button
              type="button"
              className="text-button"
              disabled={working}
              onClick={() => configure(true)}
            >
              清除金鑰
            </button>
          )}
        </form>
      </details>
      <label className="intent-toggle">
        <input
          type="checkbox"
          checked={enabled}
          disabled={!configured || working}
          onChange={(e) => onEnabled(e.target.checked)}
        />
        分析時，讓 Jev 判斷每次送出的訊息與最近上下文
      </label>
      <p className="intent-hint">
        換題會先顯示建議；資料不足則請你選擇。不使用 Jev
        也能直接選下方任務。明確的 #44／#31／#37 指令不消耗 Jev 用量。
      </p>
      {notice && (
        <p className="intent-result" role="status">
          {notice}
        </p>
      )}
    </section>
  );
}
