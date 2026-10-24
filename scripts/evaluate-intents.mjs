import { readFile } from "node:fs/promises";
import { buildRoutingRequest, decideRoute } from "../app/server/intent.mjs";
if (!process.env.TYPESAFE_API_KEY) {
  console.error(
    "尚未設定 TYPESAFE_API_KEY；未呼叫 Jev，也未執行語意準確率評估。",
  );
  process.exit(1);
}
const cases = JSON.parse(
  await readFile(
    new URL("../app/tests/fixtures/intent-evaluation.json", import.meta.url),
    "utf8",
  ),
);
let correct = 0,
  errors = 0;
for (const [i, item] of cases.entries()) {
  const started = Date.now();
  try {
    const response = await fetch("https://api.typesafe.ai/v1/systemone", {
      method: "POST",
      redirect: "error",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + process.env.TYPESAFE_API_KEY,
      },
      body: JSON.stringify(buildRoutingRequest(item)),
      signal: AbortSignal.timeout(12000),
    });
    if (!response.ok) throw new Error("service");
    const answer = (await response.json()).answers?.intent;
    const route = decideRoute(answer, item.currentTask ?? null);
    const pass = answer.choice === item.expected;
    if (pass) correct++;
    console.log(
      JSON.stringify({
        case: i + 1,
        expected: item.expected,
        choice: answer.choice,
        action: route.action,
        task: route.task,
        confidence: answer.confidence,
        pass,
        ms: Date.now() - started,
      }),
    );
  } catch {
    errors++;
    console.log(
      JSON.stringify({
        case: i + 1,
        error: "服務或回應驗證失敗",
        ms: Date.now() - started,
      }),
    );
  }
}
console.log(
  JSON.stringify({
    cases: cases.length,
    correct,
    errors,
    accuracy: correct / cases.length,
    note: "小型人工題組；非正式準確率承諾。action 與 task 需另檢查誤切換與棄權。",
  }),
);
process.exitCode = correct === cases.length ? 0 : 1;
