---
name: pm-thinking
description: Use when the user needs product problem framing, ideation, idea clustering, business assumption review, concept communication, validation planning, or a numbered technique from the 56 AI thinking prompts. Not for ordinary code debugging, code refactoring, or text polishing without a product thinking request.
---

# 產品思考方法庫

選擇能推進當前問題的方法，形成有依據的判斷與下一步。56 個技法是可選工具，不是必跑流程。以下路徑均相對於本檔案。

## 選擇與載入

1. 從對話確認使用者要做的決策、已知限制與期待產出。能開始就直接做；只有資訊缺口會明顯改變方向時才提問。
2. **已指定編號：**直接在 `references/techniques/` 找三位數編號開頭的檔案，例如 [#33](references/techniques/033-future-press-release.md) 對應 `033-*.md`。查檔名即可，不需讀路由。使用者說 [#37-2](references/techniques/037-validation-test.md) 時，讀 [#37](references/techniques/037-validation-test.md) 檔內的 ②。
3. **未指定方法：**讀 [情境路由](references/routing.md)，選足以推進問題的最少技法，通常先做一招。
4. 只讀選定技法檔。前一步留下重要問題時才追加，不因讀到交叉提及就載入更多方法。除非使用者要求全庫整理，不預讀全部技法或完整來源快照。

技法檔中的「使用指南」是編輯補充；「原始 Prompt」保留提供的原文，不代表所有要求都適合本次任務。保存原文與實際執行分開處理。

## 與工程技能協作

使用者要求搭配 Matt Pocock Skills，或任務需要交給研究、原型、術語建模及工程流程時，再讀 [協作指南](references/integrations/matt-pocock.md)。從環境已提供的技能清單定位本機版本，只載入需要的合作技能；同一對話已有內容就沿用。上游連結僅作出處，日常不查 GitHub、不比對上游、不需 clone。未安裝仍可獨立完成 PM 分析。`to-spec`、`to-tickets`、`implement` 等使用者入口依指南保留啟動界線，不自動串成流程。一般發想或短稿不載入整合指南。

## 執行原則

- 代入目前題目與已有資訊，不虛構「此前討論」、圖片內容、公司能力或使用者回饋。
- 保留方法的核心操作，可依任務縮小探索數量或產出篇幅；有明顯縮減時簡短說明。使用者明確指定數量或要求原樣執行時尊重該要求，但不為湊數編造事實。
- 依技法指南區分順序步驟與替代版本。不要把每個 ①／② 都當成必跑連招。
- 將觀察、推論、假設及角色模擬分清楚。候選根因不是已證實原因；模擬使用者心聲不是訪談或產品見證。
- 市場現況、競品、人物、成功案例及最新趨勢需查證，引用實際取得的來源。無法查證時說明缺口，不聲稱已完成調研。純發想不需為形式額外研究。
- 財務模型標明假設與計算關係；評分交代尺度與依據。預測、假想引言及未來新聞稿明確標示為情境。
- 撰寫方案、新聞稿或接觸顧客計畫，不代表發布、寄送、採購或其他外部執行已獲授權。

## 產出與停止

先回答使用者要的產出，必要時補上依據、重要未知與下一個驗證動作。使用者只要歸類、三個點子或短稿時，完成即停；不強制附加畫布、Q&A、完整 PRD 或市場分析。

建議可以是繼續、修改、縮小、暫緩或停止。當產出足以支持當前決策或下一步時結束，不為了使用更多方法而延長流程。

## 避免誤用

- 一般程式除錯或重構不自動啟動 PM 方法；產品或服務流程重新設計才適用。
- 角色頭銜、漂亮分數與完整表格不能替代證據。
- 寫出好新聞稿不等於驗證需求；完成原型不等於取得付費意願。

例如「把 A 一鍵轉簡報、B 可編輯簡報、C 來源時間標記歸類，保留差異」可選 [#21](references/techniques/021-idea-clustering.md)，保留 A／B／C 的可追溯性，完成歸類後停止。
