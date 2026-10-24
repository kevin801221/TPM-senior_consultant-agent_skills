import { routeIntent, buildRoutingRequest } from "./intent.mjs";
import http from "node:http";
import { readFile, mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve, extname } from "node:path";
import { fileURLToPath } from "node:url";
import { randomBytes, timingSafeEqual } from "node:crypto";
import { spawn, execFile } from "node:child_process";
import { promisify } from "node:util";
import { createInterface } from "node:readline";
import {
  validateRun,
  buildPrompt,
  parseAgentEvent,
  subscriptionEnv,
  commandFor,
} from "./core.mjs";
const exec = promisify(execFile);
const dist = fileURLToPath(new URL("../../dist/", import.meta.url));
const cleanError = (e) =>
  String(e?.message || e)
    .replace(/(?:sk-|ghp_|github_pat_)[\w-]+/g, "[redacted]")
    .slice(0, 800);
export async function getProviders() {
  const entries = await Promise.all(
    ["codex", "claude"].map(async (provider) => {
      try {
        const args =
          provider === "codex"
            ? ["login", "status"]
            : ["auth", "status", "--json"];
        const { stdout, stderr } = await exec(provider, args, {
          env: subscriptionEnv(),
          timeout: 12000,
          maxBuffer: 65536,
        });
        let ready = false;
        if (provider === "codex")
          ready = /Logged in using ChatGPT/i.test(stdout + stderr);
        else {
          const info = JSON.parse(stdout);
          ready =
            info.loggedIn === true &&
            ["claude.ai", "oauth"].includes(info.authMethod);
        }
        return [
          provider,
          {
            ready,
            label: ready
              ? provider === "codex"
                ? "已登入 ChatGPT"
                : "已登入 Claude 訂閱"
              : "需要訂閱帳號登入",
          },
        ];
      } catch (e) {
        return [
          provider,
          {
            ready: false,
            label: e.code === "ENOENT" ? "尚未安裝 CLI" : "需要重新登入",
            command: provider === "codex" ? "codex login" : "claude auth login",
          },
        ];
      }
    }),
  );
  return Object.fromEntries(entries);
}
export async function runAgent(data, prompt, emit, signal) {
  const directory = await mkdtemp(join(tmpdir(), "thinking-run-"));
  try {
    if (signal.aborted) throw new Error("已停止");
    await new Promise((resolveRun, rejectRun) => {
      const { command, args } = commandFor(data.provider);
      const child = spawn(command, args, {
        cwd: directory,
        env: subscriptionEnv(),
        stdio: ["pipe", "pipe", "pipe"],
        detached: process.platform !== "win32",
      });
      let errorText = "",
        failure = "",
        hasText = false,
        killTimer;
      const terminate = () => {
        try {
          process.platform === "win32"
            ? child.kill("SIGTERM")
            : process.kill(-child.pid, "SIGTERM");
        } catch {}
        killTimer = setTimeout(() => {
          try {
            process.platform === "win32"
              ? child.kill("SIGKILL")
              : process.kill(-child.pid, "SIGKILL");
          } catch {}
        }, 1500);
        killTimer.unref();
      };
      signal.addEventListener("abort", terminate, { once: true });
      if (signal.aborted) terminate();
      const timer = setTimeout(() => {
        failure = "執行超過三分鐘，請縮小問題後重試。";
        terminate();
      }, 180000);
      child.stderr.on("data", (chunk) => {
        errorText = (errorText + chunk).slice(-6000);
      });
      const lines = createInterface({ input: child.stdout });
      lines.on("line", (line) => {
        try {
          const parsed = parseAgentEvent(data.provider, JSON.parse(line));
          if (parsed?.type === "error") failure = parsed.message;
          if (parsed?.type === "text" && !signal.aborted) {
            hasText = true;
            emit(parsed);
          }
        } catch {}
      });
      child.stdin.on("error", () => {});
      child.stdin.end(prompt);
      child.once("error", (err) => {
        failure =
          err.code === "ENOENT"
            ? "找不到 " + command + "，請先安裝官方 CLI。"
            : cleanError(err);
      });
      child.once("close", (code) => {
        clearTimeout(timer);
        clearTimeout(killTimer);
        signal.removeEventListener("abort", terminate);
        lines.close();
        if (signal.aborted) rejectRun(new Error("已停止"));
        else if (failure || code !== 0 || !hasText)
          rejectRun(
            new Error(
              cleanError(
                failure || errorText || "引擎未回傳結果，請檢查登入與額度。",
              ),
            ),
          );
        else resolveRun();
      });
    });
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}
function json(res, status, value) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  });
  res.end(JSON.stringify(value));
}
async function body(req) {
  let size = 0;
  const chunks = [];
  for await (const chunk of req) {
    size += chunk.length;
    if (size > 450000) throw new Error("輸入超過大小限制。");
    chunks.push(chunk);
  }
  try {
    return JSON.parse(Buffer.concat(chunks).toString());
  } catch {
    throw new Error("無法解析輸入。");
  }
}
export function createWorkbench(options = {}) {
  const invoke = options.runAgent || runAgent,
    providers = options.getProviders || getProviders;
  const token = randomBytes(32).toString("hex");
  let active = false,
    routing = false;
  let intentKey = options.intentKey ?? process.env.TYPESAFE_API_KEY ?? "";
  const classify = options.routeIntent || routeIntent;
  const intentStatus = () => ({ configured: Boolean(intentKey) });
  const server = http.createServer(async (req, res) => {
    res.setHeader("X-Content-Type-Options", "nosniff");
    res.setHeader("Referrer-Policy", "no-referrer");
    res.setHeader(
      "Content-Security-Policy",
      "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'",
    );
    const port = server.address()?.port;
    const allowedHosts = new Set(["127.0.0.1:" + port, "localhost:" + port]);
    const host = req.headers.host;
    const origin = req.headers.origin;
    if (
      !allowedHosts.has(host) ||
      (origin &&
        !["http://127.0.0.1:" + port, "http://localhost:" + port].includes(
          origin,
        )) ||
      req.headers["sec-fetch-site"] === "cross-site"
    )
      return json(res, 403, { error: "僅允許本機工作台存取。" });
    const path = new URL(req.url, "http://" + host).pathname;
    if (req.method === "GET" && path === "/api/bootstrap") {
      try {
        return json(res, 200, {
          token,
          providers: await providers(),
          intent: intentStatus(),
        });
      } catch {
        return json(res, 503, { error: "無法檢查引擎狀態。" });
      }
    }
    if (
      req.method === "POST" &&
      ["/api/run", "/api/intent", "/api/intent/settings"].includes(path)
    ) {
      const supplied = String(req.headers["x-session-token"] || "");
      if (
        !origin ||
        Buffer.byteLength(supplied) !== Buffer.byteLength(token) ||
        !timingSafeEqual(Buffer.from(supplied), Buffer.from(token))
      )
        return json(res, 403, { error: "工作台連線已過期，請重新整理。" });
      if (!req.headers["content-type"]?.startsWith("application/json"))
        return json(res, 415, { error: "需要 JSON 輸入。" });
      if (path === "/api/intent/settings") {
        try {
          const input = await body(req);
          if (
            typeof input?.apiKey !== "string" ||
            input.apiKey.length > 512 ||
            /[^\x21-\x7e]/.test(input.apiKey)
          )
            return json(res, 400, {
              error: "金鑰格式不符；請貼上完整金鑰，不含空白。",
            });
          intentKey = input.apiKey;
          return json(res, 200, intentStatus());
        } catch {
          return json(res, 400, { error: "無法更新 Jev 設定。" });
        }
      }
      if (path === "/api/intent") {
        let state;
        try {
          state = buildRoutingRequest(await body(req)).state;
        } catch (e) {
          return json(res, 400, { error: cleanError(e) });
        }
        if (active || routing)
          return json(res, 409, { error: "正在處理其他請求，請稍後再試。" });
        routing = true;
        const controller = new AbortController();
        const cancel = () => {
          if (!res.writableEnded) controller.abort();
        };
        res.on("close", cancel);
        try {
          return json(
            res,
            200,
            await classify(state, {
              apiKey: intentKey,
              signal: controller.signal,
            }),
          );
        } catch {
          if (!res.destroyed)
            return json(res, 503, {
              error: "意圖判斷未完成，請重試或手動選擇。",
            });
        } finally {
          routing = false;
          res.off("close", cancel);
        }
        return;
      }
      let data, useJev, manualRoute;
      try {
        const raw = await body(req);
        data = validateRun(raw);
        if (
          [raw.useJev, raw.manualRoute].some(
            (v) => v !== undefined && typeof v !== "boolean",
          )
        )
          throw new Error("路由設定格式不符。");
        useJev = raw.useJev === true;
        manualRoute = raw.manualRoute === true;
      } catch (e) {
        return json(res, 400, { error: cleanError(e) });
      }
      if (active || routing)
        return json(res, 409, {
          error: "另一個工作正在執行，請等待完成或先停止。",
        });
      active = true;
      const controller = new AbortController();
      const cancel = () => {
        if (!res.writableEnded) controller.abort();
      };
      res.on("close", cancel);
      const emit = (value) => {
        if (!res.destroyed && !res.writableEnded)
          res.write(JSON.stringify(value) + "\n");
      };
      try {
        if (useJev && !manualRoute) {
          const route = await classify(
            {
              message: data.messages.at(-1).text,
              currentTask: data.task,
              decision: data.brief.decision,
              context: data.messages
                .slice(0, -1)
                .slice(-4)
                .map((m) => ({ ...m, text: m.text.slice(0, 2000) })),
            },
            { apiKey: intentKey, signal: controller.signal },
          );
          if (controller.signal.aborted) return;
          if (route.action !== "continue" || route.task !== data.task)
            return json(res, 409, { error: route.message, route });
        }
        const status = await providers();
        if (!status[data.provider]?.ready)
          return json(res, 401, {
            error:
              (data.provider === "codex" ? "Codex" : "Claude Code") +
              " 尚未使用有效訂閱登入。請在終端執行 " +
              (data.provider === "codex"
                ? "codex login"
                : "claude auth login") +
              "，再按重新檢查。",
          });
        const prompt = await buildPrompt(data);
        if (controller.signal.aborted) return;
        res.writeHead(200, {
          "Content-Type": "application/x-ndjson; charset=utf-8",
          "Cache-Control": "no-store",
        });
        res.flushHeaders();
        emit({
          type: "status",
          message: "正在以訂閱帳號分析，通常需要 20–90 秒…",
        });
        await invoke(data, prompt, emit, controller.signal);
        emit({ type: "done" });
      } catch (e) {
        if (res.headersSent) emit({ type: "error", message: cleanError(e) });
        else if (!res.destroyed) json(res, 500, { error: cleanError(e) });
      } finally {
        active = false;
        res.off("close", cancel);
        if (!res.writableEnded) res.end();
      }
      return;
    }
    if (path.startsWith("/api/"))
      return json(res, 404, { error: "找不到操作。" });
    if (req.method !== "GET" && req.method !== "HEAD")
      return json(res, 405, { error: "不支援此操作。" });
    try {
      const decoded = decodeURIComponent(path);
      const file = resolve(
        dist,
        decoded === "/" ? "index.html" : "." + decoded,
      );
      if (!file.startsWith(dist))
        return json(res, 403, { error: "無法存取。" });
      const content = await readFile(file);
      const type =
        {
          ".html": "text/html; charset=utf-8",
          ".js": "text/javascript",
          ".css": "text/css",
          ".svg": "image/svg+xml",
          ".png": "image/png",
        }[extname(file)] || "application/octet-stream";
      res.writeHead(200, { "Content-Type": type, "Cache-Control": "no-cache" });
      res.end(req.method === "HEAD" ? undefined : content);
    } catch {
      return json(res, 404, { error: "找不到頁面。請先執行 npm run build。" });
    }
  });
  return { server };
}
if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  const port = Number(process.env.PORT || 4317);
  const { server } = createWorkbench();
  server.listen(port, "127.0.0.1", () =>
    console.log("AI Thinking OS → http://127.0.0.1:" + port),
  );
  server.on("error", (error) => {
    console.error(
      error.code === "EADDRINUSE"
        ? "連接埠已使用，請設定另一個 PORT。"
        : error.message,
    );
    process.exitCode = 1;
  });
}
