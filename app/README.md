# 個人本機工作台

這是 React + assistant-ui 的本機前端，搭配 Node.js 啟動已安裝的 Codex 或 Claude Code。只監聽 127.0.0.1，不部署到雲端。

## 啟動

需要 Node.js 22.12+，以及至少一個已用訂閱帳號登入的官方 CLI。

```sh
npm install
codex login
# 若要使用 Claude：
# claude auth login
npm run build
npm start
```

開啟 http://127.0.0.1:4317 。若連接埠已使用，可用 PORT=4318 npm start。
從「釐清需求／提案預演／設計驗證」選一項，填寫決策題目、已知資訊及限制，選引擎後開始。
補充提問沿用同一任務與簡報；修改邊界時另開工作階段。完成的結果可下載 Markdown，或在本機歷史中開啟。

## Jev 意圖選招（選用）

1. 展開工作台的「連接自己的 Jev」，輸入自己的 TypeSafe API key，按「暫存金鑰」。
2. 在「想解決的問題」輸入自然語言，按「建議一個任務」，再按「套用」帶入決策欄位。
3. 檢查任務，填齊已知資訊與限制後開始分析。開啟逐輪判斷時，Jev 會在每次提交前判斷新訊息及上下文。
4. 補充留在原任務；換題、資訊不足或超出範圍會暫停分析並顯示選項。可以確認切換並檢查情境，或明確選擇本次沿用原技法。切換會完整帶入先前對話與草稿到可編輯的移轉欄位，請同步更新變更過的表單限制；超過 24,000 字需先整理，不會自動裁切。
5. 不需要 Jev 時清除金鑰，或關閉逐輪判斷。手動選招與原本的訂閱分析都可獨立使用。

金鑰只送到本機 Node 服務並存於記憶體，不回傳給前端、不寫入 localStorage／檔案／Git、不傳給 Codex 或 Claude。設定成功只代表已暫存，第一次呼叫才確認金鑰可用。可用伺服器環境變數 `TYPESAFE_API_KEY` 預設載入；清除會移除本次服務的值，若啟動環境仍有設定，重啟會重新載入。不要把金鑰貼進聊天內容或 README。

Jev 是獨立的 TypeSafe 服務，需要自己的帳號與用量；不由 Codex／Claude 訂閱代付。選招時只送輸入；逐輪判斷送目前技法 ID、決策題目、新訊息，以及最多四則先前訊息（每則最多 2,000 字）。不額外附上完整方法庫、其他成果紀錄或完整證據／限制欄位。上下文仍可能含敏感資料，啟用前請確認可以傳給 TypeSafe。

### 路由行為

- 只認開頭的明確指令：`#44 問題`、`pm-thinking #31 問題`、`/pm-thinking #37 問題`。編號與文字間需有空白。這條路徑不呼叫 Jev；段落中引用編號不視為換題指令。
- 自然語言使用官方 `POST https://api.typesafe.ai/v1/systemone`、`jev-latest` 與一個 Choice 問題。候選為三任務、`continue`、`clarify`、`out_of_scope`。
- 每次送出整則訊息判斷一次，不把段落拆成各句獨立路由。近期上下文與目前任務讓「那第二項呢？」可以被辨識為追問。
- 置信度、最高機率與前兩名差距皆需達門檻，才提出具體任務建議；目前暫定 0.7／0.75／0.25。這些是尚待實際資料校準的介面政策，不是準確率或操作授權。
- 新任務一律先由使用者套用；逐輪補充只有判定沿用同一技法才繼續。手動沿用僅略過本次分類，仍執行原技法與既有工具隔離。
- 網路錯誤、12 秒逾時、驗證失敗、格式異常回到手動選擇，不捏造判斷。
- 分類輸出只能選固定 registry ID，不能指定檔案路徑、工具、shell 指令或任意服務網址。

### Few-shot 與品質檢查

提示範例在 [intent.mjs](server/intent.mjs)，獨立評估題組在 [intent-evaluation.json](tests/fixtures/intent-evaluation.json)。提示內的範例用來表達規則；評估題組用來找出誤選、錯誤切換、超出範圍與棄權行為。

```sh
npm run check
# 在啟動終端安全設定 TYPESAFE_API_KEY 後，才執行真實服務評估：
npm run eval:intents
```

一般測試使用 fixture 驗證 API 契約與應用行為，不代表 Jev 語意準確率。真實評估會使用 TypeSafe 用量，並輸出每題的選項、路由及耗時；沒有金鑰會直接停止。請擴充自己的繁體中文案例與多輪情境，衡量錯誤切換及未命中，再調整門檻。

官方依據：[Choice](https://docs.typesafe.ai/primitives/choice)、[Confidence](https://docs.typesafe.ai/confidence)、[Skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion)、[HTTP API](https://docs.typesafe.ai/api/system-one)。

## 執行邊界

- 前後端均驗證三個固定任務與三個必填欄位，後端只載入選中的技法。
- Codex 使用 exec JSONL、read-only sandbox、停用 shell / apps / plugins / hooks / browser / multi-agent，並忽略使用者 config；認證仍由 CLI 自行管理。
- Claude 使用 restricted、空工具清單、空 MCP 設定與停用 hooks。不能把 --bare 用於訂閱登入（它限制為 API 認證）。
- 每次執行使用獨立暫存目錄，以 stdin 傳入情境，固定執行檔與參數，不透過 shell 插值。
- 同時只允許一個執行；取消、斷線或三分鐘逾時會終止子程序。
- 主題邊界是產品引導與模型指令，不能保證語意上永不偏題；工具隔離與輸入檢查另由程式實作。

## 認證與資料

使用 CLI 自己的登入。應用不讀取、不複製或儲存訂閱憑證。子程序只繼承必要環境變數，排除 API 金鑰／代理覆寫；執行前檢查訂閱登入。
題目、補充與選中的方法會送到所選模型服務；這不是離線推論。工作台只在瀏覽器 localStorage 保存最近 20 份完成結果（含情境），可在介面清除。失敗或中斷不會當作完成成果保存。
CLI 自己仍可能保留必要診斷／登入資料，依官方 CLI 行為為準。
本版預期 Codex CLI 0.164+、Claude Code 支援 --restricted 的版本；不支援舊版會顯示真實執行錯誤。

## 驗證

```sh
npm run check
```

node:test 覆蓋輸入、技法選擇、串流解析、認證環境隔離、跨來源／token 驗證、錯誤、併發與取消。HTTP 自動測試使用 fixture provider，不消耗訂閱。真實登入／額度／模型可用性需另外驗證。

## 架構選擇與來源

assistant-ui LocalRuntime 管理對話與取消，後端轉成統一 NDJSON。第一版使用 codex exec；需要完整工具核准與原生會話歷史時再改用 app-server。

- https://www.assistant-ui.com/docs/runtimes/custom/local-runtime
- https://learn.chatgpt.com/docs/non-interactive-mode
- https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan

本機訂閱串接不等同於將個人訂閱作為多人 SaaS 的共享推論後端；本版不提供多人服務。
