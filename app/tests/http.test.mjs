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
  extra = {},
) {
  const app = createWorkbench({
    runAgent,
    ...extra,
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

test("intent settings require same-origin token, never return the key, and can clear it", async (t) => {
  let received;
  const { url, headers } = await setup(t, undefined, {
    routeIntent: async (_input, options) => {
      received = options.apiKey;
      return { action: "select", task: "frame" };
    },
  });
  const post = (path, payload, custom = headers) =>
    fetch(url + path, {
      method: "POST",
      headers: custom,
      body: JSON.stringify(payload),
    });
  assert.equal(
    (
      await post(
        "/api/intent/settings",
        { apiKey: "fixture-secret" },
        { ...headers, "X-Session-Token": "" },
      )
    ).status,
    403,
  );
  assert.equal(
    (await post("/api/intent/settings", { apiKey: "fixture-secret" })).status,
    200,
  );
  const boot = await (await fetch(url + "/api/bootstrap")).json();
  assert.equal(boot.intent.configured, true);
  assert.doesNotMatch(JSON.stringify(boot), /fixture-secret/);
  assert.equal(
    (await post("/api/intent", { message: "先幫我釐清需求" })).status,
    200,
  );
  assert.equal(received, "fixture-secret");
  await post("/api/intent/settings", { apiKey: "" });
  assert.equal(
    (await (await fetch(url + "/api/bootstrap")).json()).intent.configured,
    false,
  );
});
test("per-turn route holds a proposed switch before CLI invocation; explicit manual choice resumes", async (t) => {
  let calls = 0,
    classified = 0;
  const { url, headers } = await setup(
    t,
    async (_data, _prompt, emit) => {
      calls++;
      emit({ type: "text", text: "fixture", mode: "replace" });
    },
    {
      routeIntent: async (input) => {
        classified++;
        assert.equal(input.currentTask, "frame");
        return { action: "select", task: "validate", message: "切換建議" };
      },
    },
  );
  const post = (payload) =>
    fetch(url + "/api/run", {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
    });
  const held = await post({ ...data, useJev: true });
  assert.equal(held.status, 409);
  assert.equal((await held.json()).route.task, "validate");
  assert.equal(calls, 0);
  const manual = await post({ ...data, useJev: true, manualRoute: true });
  assert.equal(manual.status, 200);
  await manual.text();
  assert.equal(calls, 1);
  assert.equal(classified, 1);
});
test("continuations use the existing skill and send only bounded routing context", async (t) => {
  let captured;
  const { url, headers } = await setup(t, undefined, {
    routeIntent: async (input) => {
      captured = input;
      return { action: "continue", task: "frame" };
    },
  });
  const r = await fetch(url + "/api/run", {
    method: "POST",
    headers,
    body: JSON.stringify({
      ...data,
      useJev: true,
      messages: [
        { role: "user", text: "first" },
        { role: "assistant", text: "a".repeat(3000) },
        { role: "user", text: "預算只有兩萬元" },
      ],
    }),
  });
  assert.equal(r.status, 200);
  await r.text();
  assert.equal(captured.context[1].text.length, 2000);
  assert.equal(captured.decision, data.brief.decision);
  assert.equal(captured.evidence, undefined);
});
test("intent API rejects malformed state and unknown destinations before model use", async (t) => {
  let calls = 0;
  const { url, headers } = await setup(t, undefined, {
    routeIntent: async () => {
      calls++;
      return { action: "manual" };
    },
  });
  const r = await fetch(url + "/api/intent", {
    method: "POST",
    headers,
    body: JSON.stringify({ message: "幫我處理問題", currentTask: "shell" }),
  });
  assert.equal(r.status, 400);
  assert.equal(calls, 0);
});
