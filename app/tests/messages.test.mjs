import { test } from "node:test";
import assert from "node:assert/strict";
import { prepareMessages, retryLatestUser } from "../src/messages.mjs";
import { validateRun } from "../server/core.mjs";
test("recovers after cancellation before any assistant text arrived", () => {
  const messages = prepareMessages([
    { id: "u1", role: "user", content: [{ type: "text", text: "開始分析" }] },
    { id: "a1", role: "assistant", content: [] },
    {
      id: "u2",
      role: "user",
      content: [{ type: "text", text: "補充：先看文件版本" }],
    },
  ]);
  assert.equal(messages.length, 2);
  assert.doesNotThrow(() =>
    validateRun({
      provider: "codex",
      task: "frame",
      brief: {
        decision: "客服流程",
        evidence: "已知資訊",
        constraints: "兩週限制",
      },
      messages,
    }),
  );
});
test("retry uses latest user as parent instead of empty assistant", () => {
  let received;
  const thread = {
    getState: () => ({
      messages: [
        { id: "u1", role: "user" },
        { id: "a1", role: "assistant" },
        { id: "u2", role: "user" },
        { id: "a2", role: "assistant" },
      ],
    }),
    startRun: (config) => {
      if (!config) throw new Error("parentId is required");
      received = config;
    },
  };
  retryLatestUser(thread);
  assert.equal(received.parentId, "u2");
});
