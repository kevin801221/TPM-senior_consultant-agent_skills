import { test } from "node:test";
import assert from "node:assert/strict";
import { createWorkbench } from "../server/index.mjs";
const data = {
  provider: "codex",
  task: "frame",
  brief: {
    decision: "選擇測試的客服流程",
    evidence: "每天查閱產品規格",
    constraints: "兩週內完成且無正式資料",
  },
  messages: [{ role: "user", text: "開始" }],
};
async function setup(
  t,
  runAgent = async (_data, _prompt, emit) => {
    emit({ type: "text", text: "test fixture", mode: "replace" });
  },
) {
  const app = createWorkbench({
    runAgent,
    getProviders: async () => ({
      codex: { ready: true, label: "已登入 ChatGPT" },
      claude: { ready: false, label: "需要登入" },
    }),
  });
  await new Promise((r) => app.server.listen(0, "127.0.0.1", r));
  t.after(
    () =>
      new Promise((r) => {
        app.server.closeAllConnections();
        app.server.close(r);
      }),
  );
  const url = "http://127.0.0.1:" + app.server.address().port;
  const boot = await (await fetch(url + "/api/bootstrap")).json();
  const headers = {
    "Content-Type": "application/json",
    Origin: url,
    "X-Session-Token": boot.token,
  };
  return { url, headers };
}
test("rejects requests from other origins and without session token", async (t) => {
  const { url, headers } = await setup(t);
  assert.equal(
    (
      await fetch(url + "/api/run", {
        method: "POST",
        headers: { ...headers, Origin: "https://evil.example" },
        body: JSON.stringify(data),
      })
    ).status,
    403,
  );
  assert.equal(
    (
      await fetch(url + "/api/run", {
        method: "POST",
        headers: { ...headers, "X-Session-Token": "" },
        body: JSON.stringify(data),
      })
    ).status,
    403,
  );
  assert.equal(
    (
      await fetch(url + "/api/bootstrap", {
        headers: { Origin: "https://evil.example" },
      })
    ).status,
    403,
  );
});
test("validates brief before starting the agent", async (t) => {
  let called = false;
  const { url, headers } = await setup(t, async () => {
    called = true;
  });
  const r = await fetch(url + "/api/run", {
    method: "POST",
    headers,
    body: JSON.stringify({ ...data, brief: {} }),
  });
  assert.equal(r.status, 400);
  assert.equal(called, false);
});
test("returns normalized stream followed by completion", async (t) => {
  const { url, headers } = await setup(t);
  const r = await fetch(url + "/api/run", {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
  const events = (await r.text()).trim().split("\n").map(JSON.parse);
  assert.equal(events[0].type, "status");
  assert.equal(events[1].text, "test fixture");
  assert.equal(events.at(-1).type, "done");
});
test("fails honestly on CLI errors rather than returning a fake result", async (t) => {
  const { url, headers } = await setup(t, async () => {
    throw new Error("subscription expired");
  });
  const r = await fetch(url + "/api/run", {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
  assert.match(await r.text(), /subscription expired/);
});
test("allows only one run and cancels work on disconnect", async (t) => {
  let canceled = false;
  const { url, headers } = await setup(
    t,
    async (_d, _p, _e, signal) =>
      new Promise((resolve) => {
        signal.addEventListener(
          "abort",
          () => {
            canceled = true;
            resolve();
          },
          { once: true },
        );
      }),
  );
  const controller = new AbortController();
  const first = await fetch(url + "/api/run", {
    method: "POST",
    headers,
    body: JSON.stringify(data),
    signal: controller.signal,
  });
  assert.equal(first.status, 200);
  assert.equal(
    (
      await fetch(url + "/api/run", {
        method: "POST",
        headers,
        body: JSON.stringify(data),
      })
    ).status,
    409,
  );
  controller.abort();
  await new Promise((resolve) => setTimeout(resolve, 60));
  assert.equal(canceled, true);
});

test("rejects non-ASCII session tokens without crashing the server", async (t) => {
  const { url, headers } = await setup(t);
  const response = await fetch(url + "/api/run", {
    method: "POST",
    headers: { ...headers, "X-Session-Token": "é".repeat(64) },
    body: JSON.stringify(data),
  });
  assert.equal(response.status, 403);
});
