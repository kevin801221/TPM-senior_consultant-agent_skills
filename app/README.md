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
