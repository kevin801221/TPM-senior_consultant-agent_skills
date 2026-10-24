import { test } from "node:test";
import assert from "node:assert/strict";
import {
  buildRoutingRequest,
  decideRoute,
  routeIntent,
} from "../server/intent.mjs";
const labels = [
  "frame",
  "critique",
  "validate",
  "continue",
  "clarify",
  "out_of_scope",
];
function answer(choice, confidence = 0.9) {
  return {
    type: "choice",
    choice,
    confidence,
    probabilities: Object.fromEntries(
      labels.map((k) => [k, k === choice ? 0.95 : 0.01]),
    ),
  };
}
test("classification includes context, few shots and an explicit no-match outcome", () => {
  const request = buildRoutingRequest({
    message: "那預算只剩兩萬元呢？",
    currentTask: "frame",
    decision: "先做哪個 AI 試點",
    context: [{ role: "assistant", text: "先研究文件查找" }],
  });
  assert.equal(request.state.currentTask, "frame");
  assert.equal(request.state.context.length, 1);
  assert.ok(request.questions.intent.criteria.out_of_scope);
  assert.ok(request.questions.intent.instructions.examples.length >= 6);
  assert.throws(() =>
    buildRoutingRequest({ message: "test", currentTask: "../../secret" }),
  );
  assert.throws(() => buildRoutingRequest({ message: "x".repeat(24001) }));
});
test("continuations stay put, switches only suggest, uncertain choices ask", () => {
  assert.equal(decideRoute(answer("continue"), "frame").action, "continue");
  assert.equal(decideRoute(answer("frame"), "frame").action, "continue");
  assert.deepEqual(
    [
      decideRoute(answer("validate"), "frame").action,
      decideRoute(answer("validate"), "frame").task,
    ],
    ["select", "validate"],
  );
  assert.equal(decideRoute(answer("critique", 0.2), null).action, "clarify");
  assert.equal(
    decideRoute(answer("out_of_scope"), null).action,
    "out_of_scope",
  );
  assert.equal(decideRoute(answer("continue"), null).action, "clarify");
});
test("invalid labels and malformed distributions cannot reach skills", () => {
  for (const invalid of [
    { ...answer("frame"), choice: "../../secret" },
    { ...answer("frame"), confidence: NaN },
    { ...answer("frame"), probabilities: { frame: 1 } },
    {
      ...answer("frame"),
      probabilities: { ...answer("frame").probabilities, validate: 0.99 },
    },
    { ...answer("frame"), type: "noul" },
  ]) {
    assert.throws(() => decideRoute(invalid, "frame"));
  }
});
test("explicit method commands bypass Jev; quoted mentions do not", async () => {
  const never = () => {
    throw new Error("must not call");
  };
  assert.equal(
    (
      await routeIntent(
        { message: "#37 幫我設計比較測試" },
        { fetchImpl: never },
      )
    ).task,
    "validate",
  );
  assert.equal(
    (
      await routeIntent(
        { message: "pm-thinking #31 幫我預演提案" },
        { fetchImpl: never },
      )
    ).task,
    "critique",
  );
  assert.equal(
    (await routeIntent({ message: "#30 檢查風險" }, { fetchImpl: never }))
      .action,
    "out_of_scope",
  );
  assert.equal(
    (
      await routeIntent(
        { message: "文件裡提到 #37，但我要處理別的" },
        { fetchImpl: never },
      )
    ).action,
    "manual",
  );
});
test("Jev HTTP uses a fixed origin, server key, bounded state and strict response", async () => {
  let captured;
  const result = await routeIntent(
    {
      message: "明天要提案，幫我預演財務主管追問",
      apiKey: "untrusted",
      context: [],
    },
    {
      apiKey: "server-secret",
      fetchImpl: async (url, options) => {
        captured = { url, ...options };
        return new Response(
          JSON.stringify({ answers: { intent: answer("critique") } }),
        );
      },
    },
  );
  assert.equal(result.task, "critique");
  assert.equal(captured.url, "https://api.typesafe.ai/v1/systemone");
  assert.equal(captured.headers.Authorization, "Bearer server-secret");
  assert.equal(captured.redirect, "error");
  assert.doesNotMatch(captured.body, /secret|untrusted/);
  assert.equal(JSON.parse(captured.body).model, "jev-latest");
});
test("upstream failures return manual choice without revealing service errors or keys", async () => {
  const result = await routeIntent(
    { message: "幫我驗證假設" },
    {
      apiKey: "super-secret",
      fetchImpl: async () => {
        throw new Error("super-secret upstream response");
      },
    },
  );
  assert.equal(result.action, "manual");
  assert.doesNotMatch(JSON.stringify(result), /super-secret|upstream response/);
  const malformed = await routeIntent(
    { message: "幫我驗證假設" },
    {
      apiKey: "key",
      fetchImpl: async () =>
        new Response(
          JSON.stringify({ answers: { intent: answer("arbitrary-command") } }),
        ),
    },
  );
  assert.equal(malformed.action, "manual");
});
