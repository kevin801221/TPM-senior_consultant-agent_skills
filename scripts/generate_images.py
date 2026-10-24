import subprocess
import os

IMG_DIR = "/Users/kevinluo/AI-Agent_video2presentations/skills/pm-thinking/assets/img"
os.makedirs(IMG_DIR, exist_ok=True)

# -------------------------------------------------------------
# Common CSS Styles
# -------------------------------------------------------------
SHARED_HEAD = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", "Noto Sans TC", "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    background: #0B1220;
    color: #F8FAFC;
    overflow: hidden;
  }
  .grid-bg {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: 
      linear-gradient(to right, rgba(255,255,255,0.035) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
  }
  .radial-glow-green {
    position: absolute;
    top: -150px; right: -100px; width: 700px; height: 700px;
    background: radial-gradient(circle, rgba(199, 250, 120, 0.09) 0%, transparent 70%);
    pointer-events: none;
  }
  .radial-glow-cyan {
    position: absolute;
    bottom: -150px; left: -100px; width: 700px; height: 700px;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, transparent 70%);
    pointer-events: none;
  }
  .pill {
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .pill-lime {
    background: #C7FA78;
    color: #0F1A12;
  }
  .pill-dark {
    background: rgba(255, 255, 255, 0.07);
    color: #94A3B8;
    border: 1px solid rgba(255, 255, 255, 0.12);
  }
</style>
"""

# -------------------------------------------------------------
# 01-hero.html
# -------------------------------------------------------------
def create_01_hero():
    html = SHARED_HEAD + """
<style>
  body {
    width: 1600px;
    height: 800px;
    padding: 50px 70px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    background: radial-gradient(circle at 75% 30%, #131E33 0%, #0B1220 70%, #060911 100%);
  }
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }
  .brand-group {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .brand-title {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #F8FAFC;
  }
  .subtitle-tag {
    font-size: 14px;
    color: #94A3B8;
    letter-spacing: 1px;
    font-weight: 500;
  }
  
  .content-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 560px;
    position: relative;
    z-index: 10;
  }

  /* Left Chaos Section */
  .chaos-section {
    width: 480px;
    height: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .chaos-header {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #64748B;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .chaos-card {
    position: absolute;
    background: rgba(23, 35, 56, 0.75);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px 20px;
    color: #CBD5E1;
    font-size: 15px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    width: 380px;
  }
  .chaos-card .tag {
    display: inline-block;
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.08);
    color: #94A3B8;
    margin-top: 8px;
    margin-right: 6px;
  }
  .c-card-1 {
    top: 50px;
    left: 10px;
    transform: rotate(-6deg);
    border-color: rgba(239, 68, 68, 0.25);
  }
  .c-card-2 {
    top: 170px;
    left: 60px;
    transform: rotate(4deg);
    border-color: rgba(234, 179, 8, 0.25);
  }
  .c-card-3 {
    top: 290px;
    left: 20px;
    transform: rotate(-3deg);
    border-color: rgba(148, 163, 184, 0.25);
  }
  .c-card-4 {
    top: 410px;
    left: 50px;
    transform: rotate(5deg);
    border-color: rgba(56, 189, 248, 0.25);
  }

  /* Center Conduit */
  .center-conduit {
    width: 140px;
    height: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .conduit-svg {
    position: absolute;
    width: 140px;
    height: 100%;
    top: 0;
    left: 0;
  }
  .conduit-pill {
    background: #0F1A12;
    border: 1px solid #C7FA78;
    color: #C7FA78;
    padding: 8px 14px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    z-index: 5;
    text-align: center;
    box-shadow: 0 0 20px rgba(199, 250, 120, 0.3);
  }

  /* Right Structured Cards */
  .order-section {
    width: 820px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .order-header {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #C7FA78;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .order-cards-grid {
    display: flex;
    gap: 20px;
  }
  .order-card {
    flex: 1;
    background: #F5F4EF;
    color: #0F172A;
    border-radius: 18px;
    padding: 28px 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 440px;
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.2);
    position: relative;
    transition: transform 0.2s ease;
  }
  .card-badge {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }
  .step-label {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #475569;
  }
  .technique-tag {
    font-size: 12px;
    font-weight: 700;
    color: #0F1A12;
    background: #C7FA78;
    padding: 4px 10px;
    border-radius: 6px;
  }
  .card-title {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #0F172A;
    margin-bottom: 12px;
    line-height: 1.25;
  }
  .card-desc {
    font-size: 15px;
    color: #475569;
    line-height: 1.55;
    flex-grow: 1;
  }
  .card-footer {
    border-top: 1px solid #E2E8F0;
    padding-top: 16px;
    margin-top: 16px;
  }
  .footer-deliverable {
    font-size: 13px;
    font-weight: 700;
    color: #047857;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .footer-sub {
    font-size: 12px;
    color: #64748B;
    margin-top: 4px;
  }

  /* Bottom bar */
  .bottom-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    color: #64748B;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 18px;
    z-index: 10;
  }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="radial-glow-green"></div>
  <div class="radial-glow-cyan"></div>

  <div class="top-bar">
    <div class="brand-group">
      <div class="pill pill-lime">FOR AI CONSULTANTS & PMs</div>
      <div class="brand-title">AI Thinking OS</div>
    </div>
    <div class="subtitle-tag">56 THINKING TECHNIQUES · 從零散想法走向清楚決策</div>
  </div>

  <div class="content-container">
    <!-- Left: Chaos -->
    <div class="chaos-section">
      <div class="chaos-header">
        <span>● 模糊需求與未定決策</span>
      </div>
      
      <div class="chaos-card c-card-1">
        <div>「客戶說想導入 AI，但需求範圍每週都在變。」</div>
        <span class="tag">模糊需求</span>
        <span class="tag">邊界不清</span>
      </div>

      <div class="chaos-card c-card-2">
        <div>「主管問：明天就要提案，憑什麼能省下成本？」</div>
        <span class="tag">缺乏證據</span>
        <span class="tag">未壓力測試</span>
      </div>

      <div class="chaos-card c-card-3">
        <div>「工作坊產出 30 個點子，會後無法收斂成決策。」</div>
        <span class="tag">思緒發散</span>
        <span class="tag">無優先級</span>
      </div>

      <div class="chaos-card c-card-4">
        <div>「Demo 看起來很炫，下一筆預算該不該繼續投入？」</div>
        <span class="tag">缺乏基準</span>
        <span class="tag">無停止條件</span>
      </div>
    </div>

    <!-- Center: Conduit -->
    <div class="center-conduit">
      <svg class="conduit-svg" viewBox="0 0 140 560" fill="none">
        <path d="M 0 100 C 70 100, 70 280, 140 280" stroke="rgba(255,255,255,0.15)" stroke-dasharray="4 4" stroke-width="2"/>
        <path d="M 0 210 C 70 210, 70 280, 140 280" stroke="#C7FA78" stroke-width="2" opacity="0.6"/>
        <path d="M 0 330 C 70 330, 70 280, 140 280" stroke="#38BDF8" stroke-width="2" opacity="0.6"/>
        <path d="M 0 450 C 70 450, 70 280, 140 280" stroke="rgba(255,255,255,0.15)" stroke-dasharray="4 4" stroke-width="2"/>
      </svg>
      <div class="conduit-pill">
        按需選招<br>收斂推進
      </div>
    </div>

    <!-- Right: Order -->
    <div class="order-section">
      <div class="order-header">
        <span>● 清楚的決策收斂架構</span>
      </div>

      <div class="order-cards-grid">
        <!-- Card 1 -->
        <div class="order-card">
          <div>
            <div class="card-badge">
              <span class="step-label">01 / FRAME</span>
              <span class="technique-tag">#44 問題切片</span>
            </div>
            <div class="card-title">拆對問題</div>
            <div class="card-desc">
              把「我們想做 AI」縮小成有對象、有情境、有具體邊界的試點題目。
            </div>
          </div>
          <div class="card-footer">
            <div class="footer-deliverable">✓ 帶走：值得先處理的題目</div>
            <div class="footer-sub">排除無邊界發散，鎖定單一關鍵環節</div>
          </div>
        </div>

        <!-- Card 2 -->
        <div class="order-card">
          <div>
            <div class="card-badge">
              <span class="step-label">02 / CHALLENGE</span>
              <span class="technique-tag">#31 模擬批評</span>
            </div>
            <div class="card-title">挑戰提案</div>
            <div class="card-desc">
              預演主管與財務的質疑視角，找出未經驗證的關鍵假設與依據缺口。
            </div>
          </div>
          <div class="card-footer">
            <div class="footer-deliverable">✓ 帶走：需要補齊的依據</div>
            <div class="footer-sub">先預演尖銳追問，提前準備防禦論點</div>
          </div>
        </div>

        <!-- Card 3 -->
        <div class="order-card">
          <div>
            <div class="card-badge">
              <span class="step-label">03 / VALIDATE</span>
              <span class="technique-tag">#37 驗證測試</span>
            </div>
            <div class="card-title">設計驗證</div>
            <div class="card-desc">
              建立現有流程基準，設計 A/B 試點並約定繼續、縮小或停止的判定門檻。
            </div>
          </div>
          <div class="card-footer">
            <div class="footer-deliverable">✓ 帶走：可以開始的下一步</div>
            <div class="footer-sub">有數據對照組，讓下一筆投入有憑有據</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="bottom-bar">
    <div>PM-THINKING · A PRACTICAL THINKING SKILL FOR AI AGENTS</div>
    <div>FRAME PROBLEMS · CHALLENGE PROPOSALS · DESIGN VALIDATION</div>
  </div>
</body>
</html>
"""
    return html

# -------------------------------------------------------------
# 02-workbench.html
# -------------------------------------------------------------
def create_02_workbench():
    html = SHARED_HEAD + """
<style>
  body {
    width: 1600px;
    height: 640px;
    padding: 40px 60px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 50% 20%, #111B2C 0%, #0B1220 70%, #060910 100%);
  }
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }
  .title-group {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .main-title {
    font-size: 22px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }
  
  .workbench-container {
    display: flex;
    gap: 30px;
    height: 480px;
    z-index: 10;
  }
  .work-zone {
    flex: 1;
    background: rgba(19, 30, 49, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    box-shadow: 0 15px 35px -10px rgba(0,0,0,0.5);
  }
  .zone-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }
  .zone-tag {
    font-size: 14px;
    font-weight: 800;
    color: #0F1A12;
    background: #C7FA78;
    padding: 4px 12px;
    border-radius: 6px;
    letter-spacing: 1px;
  }
  .zone-title {
    font-size: 15px;
    font-weight: 700;
    color: #94A3B8;
  }
  
  .desk-paper {
    background: #F5F4EF;
    color: #1E293B;
    border-radius: 12px;
    padding: 20px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    position: relative;
  }
  .paper-clip {
    position: absolute;
    top: -10px;
    left: 24px;
    width: 14px;
    height: 32px;
    border: 3px solid #94A3B8;
    border-radius: 8px;
    background: transparent;
  }
  .paper-heading {
    font-size: 17px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .sticky-note {
    background: #FEF08A;
    color: #713F12;
    padding: 10px 14px;
    border-radius: 6px;
    font-size: 13px;
    line-height: 1.4;
    font-weight: 600;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin: 8px 0;
  }
  .sticky-blue {
    background: #BAE6FD;
    color: #0369A1;
  }
  .sticky-rose {
    background: #FECDD3;
    color: #9F1239;
  }
  .metric-bar {
    background: #E2E8F0;
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 6px;
  }
  .metric-fill {
    height: 100%;
    background: #10B981;
    border-radius: 4px;
  }
  
  .paper-bottom {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px dashed #CBD5E1;
    font-size: 13px;
    font-weight: 700;
    color: #0F172A;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .zone-footer-pill {
    font-size: 12px;
    font-weight: 700;
    color: #047857;
    background: #D1FAE5;
    padding: 4px 8px;
    border-radius: 4px;
  }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="radial-glow-green"></div>
  <div class="radial-glow-cyan"></div>

  <div class="top-bar">
    <div class="title-group">
      <div class="pill pill-lime">STRATEGY WORKBENCH</div>
      <div class="main-title">AI 顧問與 PM 的策略工作現場</div>
    </div>
    <div class="pill pill-dark">三個工作區：需求訪談 · 提案預演 · 試點驗證</div>
  </div>

  <div class="workbench-container">
    <!-- Zone 1: 需求 -->
    <div class="work-zone">
      <div class="zone-header">
        <span class="zone-tag">需求</span>
        <span class="zone-title">01 需求訪談與問題拆解</span>
      </div>
      <div class="desk-paper">
        <div class="paper-clip"></div>
        <div>
          <div class="paper-heading">
            <span>客戶痛點診斷表</span>
            <span style="font-size: 12px; color: #64748B;">#44 問題切片</span>
          </div>
          <div style="font-size: 13px; color: #475569; line-height: 1.5;">
            客戶：「想導入客服 AI，但不知道從哪裡開始做起。」
          </div>
          <div class="sticky-note">
            📌 鎖定高頻場景：新進客服查詢最新產品規格，平均每次查閱耗時 8.5 分鐘。
          </div>
          <div class="sticky-note sticky-blue">
            ✂️ 切片邊界：先解單一產品手冊查核，暫不串接即時多輪客訴。
          </div>
        </div>
        <div class="paper-bottom">
          <span>核心產出</span>
          <span class="zone-footer-pill">題目明確切片</span>
        </div>
      </div>
    </div>

    <!-- Zone 2: 提案 -->
    <div class="work-zone">
      <div class="zone-header">
        <span class="zone-tag">提案</span>
        <span class="zone-title">02 提案預演與壓力測試</span>
      </div>
      <div class="desk-paper">
        <div class="paper-clip"></div>
        <div>
          <div class="paper-heading">
            <span>決策審查備忘錄</span>
            <span style="font-size: 12px; color: #64748B;">#31 模擬批評</span>
          </div>
          <div style="font-size: 13px; color: #475569; line-height: 1.5;">
            預演主管在專案審查會上的質疑觀點：
          </div>
          <div class="sticky-note sticky-rose">
            ⚠️ 財務主管質疑：「AI 產出後若仍需人工花 5 分鐘校對，總工時真有省下？」
          </div>
          <div class="sticky-note sticky-blue">
            🔍 待補證據：需建立人工核對耗時的基準線數據。
          </div>
        </div>
        <div class="paper-bottom">
          <span>核心產出</span>
          <span class="zone-footer-pill" style="background: #FEE2E2; color: #B91C1C;">防禦論點與依據缺口</span>
        </div>
      </div>
    </div>

    <!-- Zone 3: 驗證 -->
    <div class="work-zone">
      <div class="zone-header">
        <span class="zone-tag">驗證</span>
        <span class="zone-title">03 試點驗證與決策門檻</span>
      </div>
      <div class="desk-paper">
        <div class="paper-clip"></div>
        <div>
          <div class="paper-heading">
            <span>最小試點量測表</span>
            <span style="font-size: 12px; color: #64748B;">#37 驗證測試</span>
          </div>
          <div style="font-size: 13px; color: #475569; margin-bottom: 6px;">
            A/B 流程效率指標（50 筆真實常見樣本）：
          </div>
          <div style="font-size: 12px; color: #64748B; display: flex; justify-content: space-between;">
            <span>現行流程基準</span> <span>8.5 min</span>
          </div>
          <div class="metric-bar"><div class="metric-fill" style="width: 85%; background: #94A3B8;"></div></div>
          
          <div style="font-size: 12px; color: #047857; margin-top: 6px; display: flex; justify-content: space-between;">
            <span>AI 輔助流程</span> <span>2.1 min (-75%)</span>
          </div>
          <div class="metric-bar"><div class="metric-fill" style="width: 25%; background: #10B981;"></div></div>

          <div class="sticky-note" style="margin-top: 10px; background: #DCFCE7; color: #166534;">
            🎯 決策條件：耗時降幅 > 35% 繼續採購；未達標則終止。
          </div>
        </div>
        <div class="paper-bottom">
          <span>核心產出</span>
          <span class="zone-footer-pill">可執行的決策下一步</span>
        </div>
      </div>
    </div>
  </div>

    <svg style="position: absolute; top: 0; left: 0; width: 1600px; height: 720px; pointer-events: none; z-index: 20;" viewBox="0 0 1600 720" fill="none">
      <defs>
        <marker id="arrow-loop" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
          <path d="M 1 1 L 7 4 L 1 7 Z" fill="#38BDF8" />
        </marker>
      </defs>
      <path d="M 1180 550 C 1180 650, 470 650, 470 560" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="6 6" marker-end="url(#arrow-loop)" opacity="0.85"/>
      <rect x="710" y="628" width="220" height="28" rx="14" fill="#0F1E33" stroke="#38BDF8" stroke-width="1"/>
      <text x="820" y="647" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="700" letter-spacing="1">↻ 補充輸入依據 / 追加下一技法</text>
    </svg>
</body>
</html>
"""
    return html

# -------------------------------------------------------------
# 03-decision-example.html
# -------------------------------------------------------------
def create_03_decision_example():
    html = SHARED_HEAD + """
<style>
  body {
    width: 1600px;
    height: 900px;
    padding: 50px 70px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 70% 30%, #131E33 0%, #0B1220 70%, #060911 100%);
  }
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }
  .title-group {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .main-title {
    font-size: 24px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }
  
  .layout-container {
    display: flex;
    gap: 40px;
    height: 720px;
    align-items: center;
    z-index: 10;
  }

  /* Left Column: Vague Request */
  .left-col {
    width: 460px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .vague-card {
    background: rgba(23, 35, 56, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 30px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
  }
  .badge-tag {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #94A3B8;
    text-transform: uppercase;
    margin-bottom: 12px;
  }
  .vague-quote {
    font-size: 22px;
    font-weight: 700;
    color: #F8FAFC;
    line-height: 1.4;
    margin-bottom: 20px;
    border-left: 3px solid #EF4444;
    padding-left: 16px;
  }
  .scattered-issues {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .issue-item {
    font-size: 14px;
    color: #CBD5E1;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    padding: 10px 14px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .context-box {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid #38BDF8;
    border-radius: 14px;
    padding: 22px;
  }
  .context-header {
    font-size: 13px;
    font-weight: 700;
    color: #38BDF8;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .context-item {
    font-size: 13px;
    color: #E2E8F0;
    margin-bottom: 6px;
    line-height: 1.45;
  }

  /* Right Column: Progressive Steps */
  .right-col {
    flex-grow: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .step-card {
    background: #F5F4EF;
    color: #0F172A;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
    border-left: 6px solid #C7FA78;
    position: relative;
  }
  .step-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .step-index {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #0F1A12;
    background: #C7FA78;
    padding: 3px 10px;
    border-radius: 4px;
  }
  .step-tool {
    font-size: 13px;
    font-weight: 700;
    color: #64748B;
  }
  .step-title {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 8px;
  }
  .step-desc {
    font-size: 14px;
    color: #475569;
    line-height: 1.5;
    margin-bottom: 12px;
  }
  .step-outcome {
    background: #E2E8F0;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 700;
    color: #047857;
    display: flex;
    align-items: center;
    gap: 6px;
  }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="radial-glow-green"></div>
  <div class="radial-glow-cyan"></div>

  <div class="top-bar">
    <div class="title-group">
      <div class="pill pill-lime">教學示例 · WALKTHROUGH</div>
      <div class="main-title">從模糊需求到可驗證決策</div>
    </div>
    <div class="pill pill-dark">CASE: 客服 AI 導入決策演練</div>
  </div>

  <div class="layout-container">
    <!-- Left Column -->
    <div class="left-col">
      <div class="vague-card">
        <div class="badge-tag">一開始收到的需求</div>
        <div class="vague-quote">
          「我們想做客服 AI，<br>請幫忙規劃導入。」
        </div>
        <div class="scattered-issues">
          <div class="issue-item">❓ 需求範圍過大，缺乏優先場景</div>
          <div class="issue-item">❓ 尚未量測人工耗時與錯誤基準線</div>
          <div class="issue-item">❓ 盲目投入恐導致預算失控與無法驗收</div>
        </div>
      </div>

      <div class="context-box">
        <div class="context-header">💡 補上背景與邊界限制</div>
        <div class="context-item"><strong>要做的決策：</strong>是否值得投入客服 AI 試點</div>
        <div class="context-item"><strong>已知：</strong>客服常需查找產品手冊；尚無耗時 baseline</div>
        <div class="context-item"><strong>限制：</strong>2 週時間、2 位工程師、不串接正式核心系統</div>
      </div>
    </div>

    <!-- Right Column -->
    <div class="right-col">
      <!-- Step 1 -->
      <div class="step-card">
        <div class="step-meta">
          <span class="step-index">步驟 01</span>
          <span class="step-tool">#44 問題切片 (Problem Slicing)</span>
        </div>
        <div class="step-title">切出高頻切片：查找最新版產品規格</div>
        <div class="step-desc">
          不急著做全功能 AI。聚焦在「新進客服查詢最新產品規格」的高摩擦場景，避開多輪對話與情緒處理的複雜度。
        </div>
        <div class="step-outcome">
          ✓ 帶回成果：邊界清晰、適合兩週驗證的試點題目
        </div>
      </div>

      <!-- Step 2 -->
      <div class="step-card">
        <div class="step-meta">
          <span class="step-index">步驟 02</span>
          <span class="step-tool">#31 模擬批評 (Executive Critique)</span>
        </div>
        <div class="step-title">關鍵假設：包含人工核對的總耗時能顯著降低</div>
        <div class="step-desc">
          預演主管質疑：若 AI 生成答案後，客服仍需花 5 分鐘逐條對照原始手冊，總耗時並未節省。找出「缺乏人工核對時間基準」的證據缺口。
        </div>
        <div class="step-outcome">
          ✓ 帶回成果：確立端到端（含人工校對）的真實驗收標準
        </div>
      </div>

      <!-- Step 3 -->
      <div class="step-card">
        <div class="step-meta">
          <span class="step-index">步驟 03</span>
          <span class="step-tool">#37 驗證測試 (Validation Test)</span>
        </div>
        <div class="step-title">最小驗證：設計 A/B 流程試點對比</div>
        <div class="step-desc">
          抽取 50 筆常見規格查詢樣本，建立現有流程基準；事先約定評判標準：若總時間降幅 > 30% 且正確率達標則繼續，否則暫緩或停止。
        </div>
        <div class="step-outcome">
          ✓ 帶回成果：能直接帶進管理決策會議、有憑有據的試點方案
        </div>
      </div>
    </div>
  </div>

    <svg style="position: absolute; top: 0; left: 0; width: 1600px; height: 720px; pointer-events: none; z-index: 20;" viewBox="0 0 1600 720" fill="none">
      <defs>
        <marker id="arrow-loop" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
          <path d="M 1 1 L 7 4 L 1 7 Z" fill="#38BDF8" />
        </marker>
      </defs>
      <path d="M 1180 550 C 1180 650, 470 650, 470 560" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="6 6" marker-end="url(#arrow-loop)" opacity="0.85"/>
      <rect x="710" y="628" width="220" height="28" rx="14" fill="#0F1E33" stroke="#38BDF8" stroke-width="1"/>
      <text x="820" y="647" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="700" letter-spacing="1">↻ 補充輸入依據 / 追加下一技法</text>
    </svg>
</body>
</html>
"""
    return html

# -------------------------------------------------------------
# 04-method-map.html
# -------------------------------------------------------------
def create_04_method_map():
    html = SHARED_HEAD + """
<style>
  body {
    width: 1600px;
    height: 1000px;
    padding: 50px 70px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 50% 20%, #131E33 0%, #0B1220 70%, #060911 100%);
  }
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }
  .title-group {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .main-title {
    font-size: 26px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }
  
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 24px;
    height: 820px;
    z-index: 10;
  }
  .map-card {
    background: #F5F4EF;
    color: #0F172A;
    border-radius: 16px;
    padding: 26px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    position: relative;
    border-top: 5px solid #C7FA78;
  }
  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .cat-index {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #475569;
  }
  .cat-count {
    font-size: 12px;
    font-weight: 700;
    color: #0F1A12;
    background: #C7FA78;
    padding: 3px 8px;
    border-radius: 4px;
  }
  .cat-name {
    font-size: 22px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 8px;
    letter-spacing: -0.3px;
  }
  .cat-question {
    font-size: 14px;
    font-weight: 600;
    color: #0369A1;
    margin-bottom: 14px;
    background: #E0F2FE;
    padding: 6px 10px;
    border-radius: 6px;
  }
  .tech-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    flex-grow: 1;
  }
  .tech-item {
    font-size: 13px;
    color: #334155;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .tech-num {
    font-weight: 700;
    color: #0F172A;
    background: #E2E8F0;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 11px;
  }
  .card-footer {
    border-top: 1px solid #E2E8F0;
    padding-top: 12px;
    margin-top: 12px;
    font-size: 12px;
    color: #64748B;
    display: flex;
    justify-content: space-between;
  }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="radial-glow-green"></div>
  <div class="radial-glow-cyan"></div>

  <div class="top-bar">
    <div class="title-group">
      <div class="pill pill-lime">METHOD MAP</div>
      <div class="main-title">56 招思考方法地圖</div>
    </div>
    <div class="pill pill-dark">六大方法分類 · 按需選招 · 單一技法推進</div>
  </div>

  <div class="cards-grid">
    <!-- Card 1 -->
    <div class="map-card">
      <div>
        <div class="card-top">
          <span class="cat-index">01 / DISCOVERY</span>
          <span class="cat-count">#39–#53 · 15 招</span>
        </div>
        <div class="cat-name">問題釐清與受眾</div>
        <div class="cat-question">痛點在哪裡？問題怎麼切？誰會採用？</div>
        <div class="tech-list">
          <div class="tech-item"><span class="tech-num">#44</span> 分割煩惱（切出具體試點範圍）</div>
          <div class="tech-item"><span class="tech-num">#39</span> 痛點切入（找出關鍵摩擦環節）</div>
          <div class="tech-item"><span class="tech-num">#50</span> 目標客群（定義關鍵使用角色）</div>
          <div class="tech-item"><span class="tech-num">#41</span> 五個為什麼（向下挖掘根本原因）</div>
        </div>
      </div>
      <div class="card-footer">
        <span>適合情境：客戶需求模糊、範圍發散</span>
        <span style="font-weight: 700; color: #047857;">釐清題目</span>
      </div>
    </div>

    <!-- Card 2 -->
    <div class="map-card">
      <div>
        <div class="card-top">
          <span class="cat-index">02 / DIVERGENCE</span>
          <span class="cat-count">#01–#12 · 12 招</span>
        </div>
        <div class="cat-name">發散與跨域靈感</div>
        <div class="cat-question">還有什麼方向？可以借用什麼觀點？</div>
        <div class="tech-list">
          <div class="tech-item"><span class="tech-num">#03</span> 類比思考（跨產業借用成熟模式）</div>
          <div class="tech-item"><span class="tech-num">#08</span> 逆向反轉（反向思考破除直覺盲點）</div>
          <div class="tech-item"><span class="tech-num">#12</span> 跨界借鑑（引進不同領域解法）</div>
          <div class="tech-item"><span class="tech-num">#01</span> 屬性列舉（拆解要素重新排列組合）</div>
        </div>
      </div>
      <div class="card-footer">
        <span>適合情境：想法卡關、缺乏新視角</span>
        <span style="font-weight: 700; color: #047857;">激發方向</span>
      </div>
    </div>

    <!-- Card 3 -->
    <div class="map-card">
      <div>
        <div class="card-top">
          <span class="cat-index">03 / EVOLUTION</span>
          <span class="cat-count">#13–#17、#54–#56 · 8 招</span>
        </div>
        <div class="cat-name">流程改善與未來情境</div>
        <div class="cat-question">現在怎麼改？未來可能怎麼變？</div>
        <div class="tech-list">
          <div class="tech-item"><span class="tech-num">#14</span> 瓶頸突破（鎖定最大限制與塞車點）</div>
          <div class="tech-item"><span class="tech-num">#54</span> 未來回溯（從理想終局倒推必經之路）</div>
          <div class="tech-item"><span class="tech-num">#56</span> 典範轉移（預判技術破壞式變革）</div>
          <div class="tech-item"><span class="tech-num">#15</span> 價值溪流（去除流程中不必要浪費）</div>
        </div>
      </div>
      <div class="card-footer">
        <span>適合情境：現行流程塞車、規劃中長期藍圖</span>
        <span style="font-weight: 700; color: #047857;">改善瓶頸</span>
      </div>
    </div>

    <!-- Card 4 -->
    <div class="map-card">
      <div>
        <div class="card-top">
          <span class="cat-index">04 / STRUCTURING</span>
          <span class="cat-count">#18–#25 · 8 招</span>
        </div>
        <div class="cat-name">整理與具體化</div>
        <div class="cat-question">點子怎麼分群？概念還缺哪些資訊？</div>
        <div class="tech-list">
          <div class="tech-item"><span class="tech-num">#21</span> 團隊的創造力（保留編號分群點子）</div>
          <div class="tech-item"><span class="tech-num">#19</span> 概念具體化（把抽象名詞轉成具體場景）</div>
          <div class="tech-item"><span class="tech-num">#24</span> 優先級矩陣（以價值與可行性排序）</div>
          <div class="tech-item"><span class="tech-num">#22</span> 親和圖（歸納相似概念的核心模式）</div>
        </div>
      </div>
      <div class="card-footer">
        <span>適合情境：工作坊點子太多、概念空泛</span>
        <span style="font-weight: 700; color: #047857;">收斂秩序</span>
      </div>
    </div>

    <!-- Card 5 -->
    <div class="map-card">
      <div>
        <div class="card-top">
          <span class="cat-index">05 / STRESS TEST</span>
          <span class="cat-count">#26–#32 · 7 招</span>
        </div>
        <div class="cat-name">商業假設與壓力測試</div>
        <div class="cat-question">商業邏輯成立嗎？可能在哪裡失敗？</div>
        <div class="tech-list">
          <div class="tech-item"><span class="tech-num">#31</span> 模擬批評（預演財務/營運尖銳質疑）</div>
          <div class="tech-item"><span class="tech-num">#30</span> 檢測風險（找出潛在失效原因與圍欄）</div>
          <div class="tech-item"><span class="tech-num">#27</span> 價值公式（計算投入回報與商業算式）</div>
          <div class="tech-item"><span class="tech-num">#29</span> 前期驗屍（預想一年後專案為何失敗）</div>
        </div>
      </div>
      <div class="card-footer">
        <span>適合情境：準備向老闆提案、防範上線風險</span>
        <span style="font-weight: 700; color: #047857;">補齊防禦</span>
      </div>
    </div>

    <!-- Card 6 -->
    <div class="map-card">
      <div>
        <div class="card-top">
          <span class="cat-index">06 / VALIDATION</span>
          <span class="cat-count">#33–#38 · 6 招</span>
        </div>
        <div class="cat-name">表達、驗證與落地</div>
        <div class="cat-question">價值怎麼說？如何測試？下一步做什麼？</div>
        <div class="tech-list">
          <div class="tech-item"><span class="tech-num">#37</span> 驗證測試（建立對照組與決策條件）</div>
          <div class="tech-item"><span class="tech-num">#33</span> 未來新聞稿（擬定受眾看得懂的價值主張）</div>
          <div class="tech-item"><span class="tech-num">#38</span> 行動清單（將決策轉成可指派任務）</div>
          <div class="tech-item"><span class="tech-num">#35</span> 電梯簡報（用一分鐘清楚說服決策者）</div>
        </div>
      </div>
      <div class="card-footer">
        <span>適合情境：Demo 後決定去留、說服利益關係人</span>
        <span style="font-weight: 700; color: #047857;">驗證落地</span>
      </div>
    </div>
  </div>

    <svg style="position: absolute; top: 0; left: 0; width: 1600px; height: 720px; pointer-events: none; z-index: 20;" viewBox="0 0 1600 720" fill="none">
      <defs>
        <marker id="arrow-loop" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
          <path d="M 1 1 L 7 4 L 1 7 Z" fill="#38BDF8" />
        </marker>
      </defs>
      <path d="M 1180 550 C 1180 650, 470 650, 470 560" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="6 6" marker-end="url(#arrow-loop)" opacity="0.85"/>
      <rect x="710" y="628" width="220" height="28" rx="14" fill="#0F1E33" stroke="#38BDF8" stroke-width="1"/>
      <text x="820" y="647" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="700" letter-spacing="1">↻ 補充輸入依據 / 追加下一技法</text>
    </svg>
</body>
</html>
"""
    return html

# -------------------------------------------------------------
# 05-skill-flow.html
# -------------------------------------------------------------
def create_05_skill_flow():
    html = SHARED_HEAD + """
<style>
  body {
    width: 1600px;
    height: 720px;
    padding: 40px 60px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 60% 40%, #111C30 0%, #0B1220 70%, #060910 100%);
  }
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }
  .title-group {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .main-title {
    font-size: 24px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }
  
  .flow-container {
    display: flex;
    height: 520px;
    align-items: center;
    position: relative;
    z-index: 10;
  }

  /* 4 Main Pipeline Steps */
  .pipeline-steps {
    display: flex;
    align-items: center;
    gap: 16px;
    width: 1100px;
  }
  .step-node {
    flex: 1;
    background: #F5F4EF;
    color: #0F172A;
    border-radius: 14px;
    padding: 22px 18px;
    height: 380px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    position: relative;
    border-top: 4px solid #C7FA78;
  }
  .step-tag-pill {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    background: #0F1A12;
    color: #C7FA78;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
  }
  .node-title {
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 12px;
    line-height: 1.3;
  }
  .node-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex-grow: 1;
  }
  .node-item {
    font-size: 13px;
    color: #475569;
    line-height: 1.4;
    background: #E2E8F0;
    padding: 6px 10px;
    border-radius: 6px;
  }
  .node-footer {
    font-size: 12px;
    font-weight: 700;
    color: #047857;
    border-top: 1px solid #CBD5E1;
    padding-top: 8px;
    margin-top: 8px;
  }

  /* Connecting arrow */
  .flow-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #C7FA78;
    font-size: 20px;
    font-weight: bold;
  }

  /* Fork Outcomes */
  .fork-outcomes {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 440px;
    width: 360px;
    margin-left: 24px;
  }
  .outcome-box {
    border-radius: 14px;
    padding: 20px 24px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
  }
  .outcome-success {
    background: #0F291E;
    border: 2px solid #C7FA78;
    color: #F8FAFC;
  }
  .outcome-loop {
    background: rgba(30, 41, 59, 0.8);
    border: 1px dashed #38BDF8;
    color: #CBD5E1;
  }
  .outcome-badge {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 6px;
  }
  .outcome-title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 8px;
  }
  .outcome-desc {
    font-size: 13px;
    line-height: 1.45;
  }

  /* Connector Loop line */
  .loop-connector {
    position: absolute;
    bottom: 20px;
    left: 200px;
    width: 1040px;
    height: 40px;
    pointer-events: none;
  }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="radial-glow-green"></div>
  <div class="radial-glow-cyan"></div>

  <div class="top-bar">
    <div class="title-group">
      <div class="pill pill-lime">AGENT WORKFLOW</div>
      <div class="main-title">Skill 運作流程：按需選招，推進即停</div>
    </div>
    <div class="pill pill-dark">依情境選用 · 依據與假設分離 · 產出適量 · 隨時可停</div>
  </div>

  <div class="flow-container">
    <div class="pipeline-steps">
      <!-- Node 1 -->
      <div class="step-node">
        <div>
          <span class="step-tag-pill">01 / INPUT</span>
          <div class="node-title">帶入難題與限制</div>
          <div class="node-items">
            <div class="node-item"><strong>角色：</strong>AI 顧問 / 資深 PM</div>
            <div class="node-item"><strong>決策：</strong>現在需要決定什麼</div>
            <div class="node-item"><strong>已知：</strong>現有數據與事實</div>
            <div class="node-item"><strong>限制：</strong>時間、人力、預算</div>
          </div>
        </div>
        <div class="node-footer">以決策為導向</div>
      </div>

      <div class="flow-arrow">➔</div>

      <!-- Node 2 -->
      <div class="step-node">
        <div>
          <span class="step-tag-pill">02 / ROUTE</span>
          <div class="node-title">情境選招</div>
          <div class="node-items">
            <div class="node-item">查閱情境路由導航</div>
            <div class="node-item">或直接指定技法編號</div>
            <div class="node-item"><strong>原則：</strong>一次只挑最能推進問題的一招</div>
          </div>
        </div>
        <div class="node-footer">按需精準加載</div>
      </div>

      <div class="flow-arrow">➔</div>

      <!-- Node 3 -->
      <div class="step-node">
        <div>
          <span class="step-tag-pill">03 / EXECUTE</span>
          <div class="node-title">讀取技法 Prompt</div>
          <div class="node-items">
            <div class="node-item">僅載入該技法指南</div>
            <div class="node-item"><strong>標註：</strong>事實、推論與假設</div>
            <div class="node-item">絕不強迫跑完全套流程</div>
          </div>
        </div>
        <div class="node-footer">讓依據清晰可辨</div>
      </div>

      <div class="flow-arrow">➔</div>

      <!-- Node 4 -->
      <div class="step-node">
        <div>
          <span class="step-tag-pill">04 / DECISION</span>
          <div class="node-title">判斷／下一步</div>
          <div class="node-items">
            <div class="node-item">產出明確可執行行動</div>
            <div class="node-item">評估現有依據是否充足</div>
            <div class="node-item">決定立即推進或補充驗證</div>
          </div>
        </div>
        <div class="node-footer">推進行動成果</div>
      </div>
    </div>

    <!-- Fork Outcomes -->
    <div class="fork-outcomes">
      <!-- Success / Stop -->
      <div class="outcome-box outcome-success">
        <div class="outcome-badge" style="color: #C7FA78;">✓ 已足夠推進 (SUFFICIENT)</div>
        <div class="outcome-title" style="color: #C7FA78;">【完成任務 STOP】</div>
        <div class="outcome-desc" style="color: #E2E8F0;">
          保持產出適量，一次推進一個具體決策。帶著產出安排訪談、補齊提案或規劃最小測試。
        </div>
      </div>

      <!-- Loopback -->
      <div class="outcome-box outcome-loop">
        <div class="outcome-badge" style="color: #38BDF8;">↻ 仍有重大缺口 (GAPS REMAIN)</div>
        <div class="outcome-title" style="color: #F8FAFC;">補資訊或追加方法</div>
        <div class="outcome-desc">
          僅在前一步留下不可忽視的未知風險時，才追加下一步技法或回流補充輸入。
        </div>
      </div>
    </div>
  </div>

    <svg style="position: absolute; top: 0; left: 0; width: 1600px; height: 720px; pointer-events: none; z-index: 20;" viewBox="0 0 1600 720" fill="none">
      <defs>
        <marker id="arrow-loop" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
          <path d="M 1 1 L 7 4 L 1 7 Z" fill="#38BDF8" />
        </marker>
      </defs>
      <path d="M 1180 550 C 1180 650, 470 650, 470 560" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="6 6" marker-end="url(#arrow-loop)" opacity="0.85"/>
      <rect x="710" y="628" width="220" height="28" rx="14" fill="#0F1E33" stroke="#38BDF8" stroke-width="1"/>
      <text x="820" y="647" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="700" letter-spacing="1">↻ 補充輸入依據 / 追加下一技法</text>
    </svg>
</body>
</html>
"""
    return html

# -------------------------------------------------------------
# Generate HTML and Render PNGs
# -------------------------------------------------------------
files = [
    ("01-hero.html", create_01_hero(), f"{IMG_DIR}/01-hero.png", 1600, 800),
    ("02-workbench.html", create_02_workbench(), f"{IMG_DIR}/02-workbench.png", 1600, 640),
    ("03-decision-example.html", create_03_decision_example(), f"{IMG_DIR}/03-decision-example.png", 1600, 900),
    ("04-method-map.html", create_04_method_map(), f"{IMG_DIR}/04-method-map.png", 1600, 1000),
    ("05-skill-flow.html", create_05_skill_flow(), f"{IMG_DIR}/05-skill-flow.png", 1600, 720),
]

for html_name, html_content, out_png, w, h in files:
    tmp_html = f"/tmp/{html_name}"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=1",
        f"--window-size={w},{h}",
        "--hide-scrollbars",
        f"--screenshot={out_png}",
        f"file://{tmp_html}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS: {out_png} ({w}x{h})")
    else:
        print(f"FAILED: {out_png}: {res.stderr}")

print("All tasks completed.")
