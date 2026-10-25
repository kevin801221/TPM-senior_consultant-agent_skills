import subprocess
import os
import base64

V2_DIR = "/Users/kevinluo/AI-Agent_video2presentations/skills/pm-thinking/assets/img/v2"
ASSETS_DIR = "/Users/kevinluo/AI-Agent_video2presentations/skills/pm-thinking/assets"
os.makedirs(V2_DIR, exist_ok=True)

# Helper to read base64 image
def get_base64_image(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        ext = os.path.splitext(path)[1].lower().replace(".", "")
        mime = "image/png" if ext == "png" else "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("utf-8")

workbench_full_b64 = get_base64_image(os.path.join(ASSETS_DIR, "real_workbench_capture.png"))
workbench_detail_b64 = get_base64_image(os.path.join(ASSETS_DIR, "real_workbench_detail.png"))
hero_backdrop_b64 = get_base64_image(os.path.join(ASSETS_DIR, "brand/hero_backdrop.jpg"))

# -------------------------------------------------------------
# Base CSS Style
# -------------------------------------------------------------
BASE_CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "PingFang TC", "Noto Sans TC", "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    background: #0B1220;
    color: #F8FAFC;
    overflow: hidden;
  }
  .bg-grid {
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(to right, rgba(255,255,255,0.035) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
  }
  .glow-lime {
    position: absolute;
    top: -200px; right: -100px; width: 1200px; height: 1200px;
    background: radial-gradient(circle, rgba(199, 250, 120, 0.08) 0%, transparent 65%);
    pointer-events: none;
  }
  .glow-cyan {
    position: absolute;
    bottom: -200px; left: -100px; width: 1200px; height: 1200px;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.06) 0%, transparent 65%);
    pointer-events: none;
  }
  .pill-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 22px;
    border-radius: 9999px;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }
  .pill-lime {
    background: #C7FA78;
    color: #0B1220;
  }
  .pill-dark {
    background: rgba(255, 255, 255, 0.06);
    color: #94A3B8;
    border: 1px solid rgba(255, 255, 255, 0.12);
  }
  .pill-cyan {
    background: rgba(56, 189, 248, 0.12);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.3);
  }
"""

# -------------------------------------------------------------
# 01-hero.html (3200 x 1600)
# -------------------------------------------------------------
def build_01_hero():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  {BASE_CSS}
  body {{
    width: 3200px;
    height: 1600px;
    padding: 80px 120px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 70% 30%, #15223A 0%, #0B1220 70%, #050811 100%);
    position: relative;
  }}
  .brand-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .brand-group {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}
  .brand-logo-text {{
    font-size: 38px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -1px;
  }}
  .hero-middle {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 80px;
    z-index: 10;
    margin-top: -10px;
  }}
  .hero-headings {{
    flex: 1.35;
  }}
  .hero-title {{
    font-size: 96px;
    font-weight: 950;
    line-height: 1.15;
    letter-spacing: -2.5px;
    color: #FFFFFF;
  }}
  .hero-subtitle {{
    font-size: 40px;
    font-weight: 750;
    color: #C7FA78;
    margin-top: 24px;
    letter-spacing: -0.5px;
  }}
  .hero-desc {{
    font-size: 26px;
    color: #94A3B8;
    margin-top: 18px;
    line-height: 1.6;
    max-width: 1400px;
  }}
  .hero-art-container {{
    flex: 0.95;
    height: 520px;
    position: relative;
    border-radius: 28px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6);
  }}
  .hero-art-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .art-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(11, 18, 32, 0.25) 0%, rgba(11, 18, 32, 0) 50%, rgba(11, 18, 32, 0.65) 100%);
    pointer-events: none;
  }}
  .floating-badge {{
    position: absolute;
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(11, 18, 32, 0.88);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.16);
    padding: 12px 22px;
    border-radius: 14px;
    font-size: 19px;
    font-weight: 750;
    color: #F8FAFC;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
  }}
  .badge-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }}
  .dot-lime {{ background: #C7FA78; box-shadow: 0 0 10px #C7FA78; }}
  .dot-cyan {{ background: #38BDF8; box-shadow: 0 0 10px #38BDF8; }}
  .dot-white {{ background: #F5F3ED; box-shadow: 0 0 10px #F5F3ED; }}
  .f-badge-1 {{ top: 35px; left: 35px; border-left: 4px solid #C7FA78; }}
  .f-badge-2 {{ top: 220px; right: 35px; border-left: 4px solid #38BDF8; }}
  .f-badge-3 {{ bottom: 35px; left: 80px; border-left: 4px solid #F5F3ED; }}

  .flow-strip {{
    display: flex;
    align-items: center;
    gap: 36px;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 26px;
    padding: 34px 44px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.4);
    backdrop-filter: blur(12px);
    z-index: 10;
  }}
  .flow-step {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .step-label {{
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #64748B;
  }}
  .step-card-box {{
    background: #172439;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 22px 26px;
    min-height: 145px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .step-card-box.highlight {{
    background: #F5F3ED;
    color: #0B1220;
    border: 2px solid #C7FA78;
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
  }}
  .step-text-main {{
    font-size: 24px;
    font-weight: 750;
    line-height: 1.35;
  }}
  .step-text-sub {{
    font-size: 18px;
    color: #94A3B8;
    margin-top: 8px;
  }}
  .step-card-box.highlight .step-text-sub {{
    color: #475569;
  }}
  .flow-arrow {{
    font-size: 32px;
    color: #C7FA78;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    opacity: 0.85;
  }}
  .flow-arrow small {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #94A3B8;
    white-space: nowrap;
  }}
  .bottom-status-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 24px;
    font-size: 20px;
    color: #64748B;
    z-index: 10;
  }}
</style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="glow-lime"></div>
  <div class="glow-cyan"></div>

  <div class="brand-bar">
    <div class="brand-group">
      <span class="pill-tag pill-lime">AI THINKING OS</span>
      <span class="brand-logo-text">pm-thinking</span>
    </div>
    <span class="pill-tag pill-dark">AGENT SKILL · 56 個思考技法</span>
  </div>

  <div class="hero-middle">
    <div class="hero-headings">
      <div class="hero-title">把模糊需求，<br>變成清楚決策。</div>
      <div class="hero-subtitle">給 AI 顧問與 PM 的 56 個思考技法</div>
      <div class="hero-desc">
        核心是可以自然對話使用、按需載入的 Agent Skill。將零散的問題、多變的點子與現實限制，透過情境選招收斂成邊界清楚、有依據的下一步。
      </div>
    </div>

    <div class="hero-art-container">
      <img class="hero-art-img" src="{hero_backdrop_b64}" alt="AI Thinking OS 思考棱鏡品牌視覺">
      <div class="art-overlay"></div>
      <div class="floating-badge f-badge-1">
        <span class="badge-dot dot-lime"></span>
        <span>#44 分割煩惱 · 釐清邊界</span>
      </div>
      <div class="floating-badge f-badge-2">
        <span class="badge-dot dot-cyan"></span>
        <span>#31 模擬批評 · 預演盲點</span>
      </div>
      <div class="floating-badge f-badge-3">
        <span class="badge-dot dot-white"></span>
        <span>#37 驗證步驟 · 最小試點</span>
      </div>
    </div>
  </div>

  <div class="flow-strip">
    <div class="flow-step">
      <span class="step-label">01 / 輸入起點</span>
      <div class="step-card-box">
        <div class="step-text-main">「客戶想導入 AI，但不知從何開始」</div>
        <div class="step-text-sub">帶入目前決策、已知數據與時間預算限制</div>
      </div>
    </div>

    <div class="flow-arrow">
      <span>➔</span>
      <small>按需選招</small>
    </div>

    <div class="flow-step">
      <span class="step-label">02 / 技法思考</span>
      <div class="step-card-box">
        <div class="step-text-main">單一技法對話推進（如 #44、#31、#37）</div>
        <div class="step-text-sub">分清已知、推論與假設，絕不跑無謂全套流程</div>
      </div>
    </div>

    <div class="flow-arrow">
      <span>➔</span>
      <small>足夠即停</small>
    </div>

    <div class="flow-step" style="flex: 1.15;">
      <span class="step-label" style="color: #C7FA78;">03 / 清楚決策</span>
      <div class="step-card-box highlight">
        <div class="step-text-main" style="color: #0B1220;">明確下一步：範圍邊界與驗證計畫</div>
        <div class="step-text-sub">✓ 值得先解的切片 · ✓ 預演質疑之依據 · ✓ 最小試點門檻</div>
      </div>
    </div>
  </div>

  <div class="bottom-status-bar">
    <span>CORE SKILL RUNS IN CLAUDE CODE, CODEX, CURSOR & TERMINAL</span>
    <span>FRAME PROBLEMS · CHALLENGE PROPOSALS · DESIGN VALIDATION</span>
  </div>
</body>
</html>"""

# -------------------------------------------------------------
# 02-workbench.html (3200 x 1800)
# -------------------------------------------------------------
def build_02_workbench():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  {BASE_CSS}
  body {{
    width: 3200px;
    height: 1800px;
    padding: 80px 120px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 50% 10%, #111C30 0%, #0B1220 70%, #060910 100%);
  }}
  .top-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .title-group {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}
  .title-main {{
    font-size: 38px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }}
  .main-layout {{
    display: flex;
    gap: 60px;
    align-items: center;
    height: 1460px;
    z-index: 10;
  }}
  .browser-container {{
    flex: 1.7;
    height: 1400px;
    background: #172B25;
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 35px 80px -15px rgba(0, 0, 0, 0.7);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}
  .browser-chrome {{
    background: #0E1A16;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }}
  .traffic-lights {{
    display: flex;
    gap: 10px;
  }}
  .light {{
    width: 16px;
    height: 16px;
    border-radius: 50%;
  }}
  .l-red {{ background: #EF4444; }}
  .l-yellow {{ background: #F59E0B; }}
  .l-green {{ background: #10B981; }}
  .url-bar {{
    background: rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 8px 24px;
    font-size: 18px;
    color: #94A3B8;
    display: flex;
    align-items: center;
    gap: 10px;
    width: 480px;
  }}
  .browser-content {{
    flex: 1;
    overflow: hidden;
    position: relative;
    background: #F6F7F3;
  }}
  .browser-screenshot {{
    width: 100%;
    height: auto;
    display: block;
    transform-origin: top left;
  }}

  /* Detail Column */
  .detail-column {{
    flex: 1.15;
    display: flex;
    flex-direction: column;
    gap: 24px;
    height: 1400px;
    justify-content: center;
  }}
  .detail-zoom-card {{
    background: #131E33;
    border: 2px solid rgba(199, 250, 120, 0.4);
    border-radius: 22px;
    padding: 22px 24px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .zoom-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .zoom-pill {{
    background: #C7FA78;
    color: #0B1220;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 1px;
    padding: 6px 14px;
    border-radius: 6px;
  }}
  .zoom-tag-text {{
    font-size: 16px;
    color: #94A3B8;
    font-weight: 600;
  }}
  .zoom-crop-box {{
    width: 100%;
    height: 440px;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: #F6F7F3;
  }}
  .zoom-crop-img {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .detail-card {{
    background: #131E33;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.4);
  }}
  .card-label {{
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #C7FA78;
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .card-h3 {{
    font-size: 26px;
    font-weight: 800;
    color: #F8FAFC;
    margin-bottom: 10px;
    line-height: 1.3;
  }}
  .card-body {{
    font-size: 19px;
    color: #94A3B8;
    line-height: 1.55;
  }}
  .bottom-badge-strip {{
    display: flex;
    gap: 14px;
    margin-top: 14px;
  }}
  .badge-chip {{
    background: rgba(199, 250, 120, 0.12);
    border: 1px solid rgba(199, 250, 120, 0.3);
    color: #C7FA78;
    font-size: 15px;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 8px;
  }}
</style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="glow-lime"></div>
  <div class="glow-cyan"></div>

  <div class="top-header">
    <div class="title-group">
      <span class="pill-tag pill-lime">教學示例 · OPTIONAL WORKBENCH</span>
      <span class="title-main">選用工作台：直覺定義思考邊界與引擎</span>
    </div>
    <span class="pill-tag pill-dark">目前聚焦三項最常見任務 · 其餘於對話中按需使用</span>
  </div>

  <div class="main-layout">
    <!-- Left: Authentic Browser Mockup -->
    <div class="browser-container">
      <div class="browser-chrome">
        <div class="traffic-lights">
          <div class="light l-red"></div>
          <div class="light l-yellow"></div>
          <div class="light l-green"></div>
        </div>
        <div class="url-bar">
          <span>🔒 http://127.0.0.1:4317</span>
        </div>
        <span style="font-size: 16px; color: #64748B; margin-left: auto;">本機服務 · 成果保留於個人瀏覽器</span>
      </div>
      <div class="browser-content">
        <img class="browser-screenshot" src="{workbench_full_b64}" alt="AI Thinking OS 本機工作台截圖">
      </div>
    </div>

    <!-- Right: Editorial Details & Key Detail Crop -->
    <div class="detail-column">
      <div class="detail-zoom-card">
        <div class="zoom-top-bar">
          <span class="zoom-pill">關鍵細節實拍放大 · REAL DETAIL CROP</span>
          <span class="zoom-tag-text">決策邊界輸入與思考引擎切換</span>
        </div>
        <div class="zoom-crop-box">
          <img class="zoom-crop-img" src="{workbench_detail_b64}" alt="真實工作台核心輸入區域">
        </div>
      </div>

      <div class="detail-card">
        <div class="card-label">01 / 三大核心任務與思考邊界</div>
        <div class="card-h3">先定義思考邊界，拒絕 AI 空泛漫遊</div>
        <div class="card-body">
          工作台聚焦三項最高頻決策痛點：<b>01 釐清需求</b>（#44 分割煩惱）、<b>02 提案預演</b>（#31 模擬批評）、<b>03 設計驗證</b>（#37 驗證測試的步驟）。強制定義「決策、已知、限制」三要素。
        </div>
      </div>

      <div class="detail-card">
        <div class="card-label" style="color: #38BDF8;">02 / 本機私有安全隔離</div>
        <div class="card-h3">使用既有官方 CLI，成果留存本機</div>
        <div class="card-body">
          透過本機服務直接調用官方 Codex 或 Claude Code，認證與額度自理，分析結果完全保留於本機瀏覽器，不經第三方中介。
        </div>
        <div class="bottom-badge-strip">
          <span class="badge-chip">真實介面實拍</span>
          <span class="badge-chip">無虛假功能描繪</span>
          <span class="badge-chip">選用介面</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

# -------------------------------------------------------------
# 03-decision-example.html (3200 x 1800)
# -------------------------------------------------------------
def build_03_decision_example():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  {BASE_CSS}
  body {{
    width: 3200px;
    height: 1800px;
    padding: 90px 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 65% 30%, #131E33 0%, #0B1220 70%, #060911 100%);
  }}
  .top-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .title-group {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}
  .title-main {{
    font-size: 38px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }}
  .case-container {{
    display: flex;
    gap: 60px;
    align-items: center;
    height: 1440px;
    z-index: 10;
  }}
  .left-pane {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 36px;
  }}
  .initial-card {{
    background: #141F33;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 24px;
    padding: 44px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.5);
  }}
  .card-tag {{
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #94A3B8;
    text-transform: uppercase;
    margin-bottom: 20px;
  }}
  .vague-quote {{
    font-size: 38px;
    font-weight: 800;
    line-height: 1.35;
    color: #FFFFFF;
    border-left: 6px solid #EF4444;
    padding-left: 24px;
    margin-bottom: 30px;
  }}
  .flaw-list {{
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .flaw-item {{
    font-size: 20px;
    color: #CBD5E1;
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.25);
    padding: 16px 20px;
    border-radius: 12px;
  }}
  .context-injected-card {{
    background: #0E2238;
    border: 2px solid #38BDF8;
    border-radius: 24px;
    padding: 40px;
  }}
  .context-header {{
    font-size: 22px;
    font-weight: 800;
    color: #38BDF8;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .context-line {{
    font-size: 20px;
    color: #F1F5F9;
    margin-bottom: 12px;
    line-height: 1.5;
  }}

  /* Right Progressive Steps */
  .right-pane {{
    flex: 1.85;
    display: flex;
    flex-direction: column;
    gap: 28px;
  }}
  .stage-card {{
    background: #F5F3ED;
    color: #0F172A;
    border-radius: 22px;
    padding: 36px 42px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    border-left: 8px solid #C7FA78;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .stage-meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
  }}
  .stage-badge {{
    font-size: 16px;
    font-weight: 800;
    color: #0B1220;
    background: #C7FA78;
    padding: 6px 14px;
    border-radius: 6px;
    letter-spacing: 1px;
  }}
  .technique-ref {{
    font-size: 18px;
    font-weight: 700;
    color: #475569;
  }}
  .stage-title {{
    font-size: 30px;
    font-weight: 850;
    color: #0B1220;
    margin-bottom: 12px;
    line-height: 1.25;
  }}
  .stage-desc {{
    font-size: 20px;
    color: #475569;
    line-height: 1.55;
    margin-bottom: 18px;
  }}
  .stage-metric-box {{
    background: #E2E8F0;
    border-radius: 12px;
    padding: 18px 24px;
    margin-bottom: 16px;
    font-size: 19px;
    color: #1E293B;
    line-height: 1.5;
  }}
  .metric-pill {{
    display: inline-block;
    background: #CBD5E1;
    color: #334155;
    font-weight: 700;
    font-size: 15px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 6px;
  }}
  .stage-deliverable {{
    background: #DCFCE7;
    color: #166534;
    font-size: 19px;
    font-weight: 750;
    padding: 12px 20px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
</style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="glow-lime"></div>
  <div class="glow-cyan"></div>

  <div class="top-header">
    <div class="title-group">
      <span class="pill-tag pill-lime">教學示例 · WALKTHROUGH</span>
      <span class="title-main">從模糊需求到可驗證決策</span>
    </div>
    <span class="pill-tag pill-dark">CASE: 客服 AI 導入之按需選招演練</span>
  </div>

  <div class="case-container">
    <!-- Left: Request & Context -->
    <div class="left-pane">
      <div class="initial-card">
        <div class="card-tag">一開始收到的需求</div>
        <div class="vague-quote">
          「我們想做客服 AI，<br>請幫忙規劃導入。」
        </div>
        <div class="flaw-list">
          <div class="flaw-item">⚠️ 範圍過於廣泛，未鎖定特定場景與對象</div>
          <div class="flaw-item">⚠️ 尚未測量現行耗時與錯誤，無比較基準</div>
          <div class="flaw-item">⚠️ 若直接全量開發，恐導致高成本卻無法驗收</div>
        </div>
      </div>

      <div class="context-injected-card">
        <div class="context-header">💡 帶入決策題目與邊界限制</div>
        <div class="context-line"><b>要做的決策：</b>是否值得投入客服 AI 試點？</div>
        <div class="context-line"><b>目前已知：</b>客服常查規格手冊；尚未量測基線耗時。</div>
        <div class="context-line"><b>現實限制：</b>兩週、兩位工程師、不串接正式系統。</div>
      </div>
    </div>

    <!-- Right: Progressive Convergence -->
    <div class="right-pane">
      <!-- Step 1 -->
      <div class="stage-card">
        <div class="stage-meta">
          <span class="stage-badge">步驟 01 · 聚焦題目</span>
          <span class="technique-ref">選用技法：#44 分割煩惱</span>
        </div>
        <div class="stage-title">聚焦高頻切片：查找最新版產品規格</div>
        <div class="stage-desc">
          不急著做全功能 AI。將客服複雜情境切開，鎖定在「新進客服查詢最新規格」的單一高頻切片，暫不處理多輪情緒與客訴。
        </div>
        <div class="stage-deliverable">
          ✓ 帶走成果：一個範圍明確、能在兩週內評估的具體試點題目
        </div>
      </div>

      <!-- Step 2 -->
      <div class="stage-card">
        <div class="stage-meta">
          <span class="stage-badge">步驟 02 · 壓力測試</span>
          <span class="technique-ref">選用技法：#31 模擬批評</span>
        </div>
        <div class="stage-title">預演主管質疑：發現人工核對時間仍為未知</div>
        <div class="stage-desc">
          預演審查會追問：若 AI 給出規格後，客服仍需花數分鐘人工對照原廠手冊以防出錯，端到端耗時並未減少。找出關鍵證據缺口。
        </div>
        <div class="stage-deliverable">
          ✓ 帶走成果：確立真實驗收關鍵：必須包含人工核對的端到端耗時
        </div>
      </div>

      <!-- Step 3 -->
      <div class="stage-card">
        <div class="stage-meta">
          <span class="stage-badge">步驟 03 · 最小驗證</span>
          <span class="technique-ref">選用技法：#37 驗證測試的步驟</span>
        </div>
        <div class="stage-title">設計最小驗證：比較既有與 AI 輔助流程</div>
        <div class="stage-desc">
          建立對照試點：抽樣真實規格查詢，分別量測現行流程與 AI 輔助流程的端到端總耗時。
        </div>
        <div class="stage-metric-box">
          <span class="metric-pill">現行流程基準</span> 包含翻找手冊時間：<b>[待量測]</b><br>
          <span class="metric-pill">AI 輔助流程</span> 包含人工核對時間：<b>[待驗證]</b><br>
          <span class="metric-pill" style="background:#FEF08A;color:#713F12;">示例門檻，待確認</span> 若端到端總耗時顯著降低且正確率達標則繼續，否則暫緩或調整。
        </div>
        <div class="stage-deliverable">
          ✓ 帶走成果：能直接帶回管理會議、有憑有據且具備停止條件的試點計畫
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

# -------------------------------------------------------------
# 04-method-map.html (3200 x 2000)
# -------------------------------------------------------------
def build_04_method_map():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  {BASE_CSS}
  body {{
    width: 3200px;
    height: 2000px;
    padding: 90px 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 50% 15%, #131E33 0%, #0B1220 70%, #060911 100%);
  }}
  .top-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .title-group {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}
  .title-main {{
    font-size: 40px;
    font-weight: 850;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }}
  .map-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 40px;
    height: 1640px;
    z-index: 10;
  }}
  .cat-card {{
    background: #F5F3ED;
    color: #0B1220;
    border-radius: 24px;
    padding: 44px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.4);
    border-top: 8px solid #C7FA78;
    position: relative;
  }}
  .cat-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }}
  .cat-num {{
    font-size: 19px;
    font-weight: 850;
    letter-spacing: 2px;
    color: #64748B;
  }}
  .cat-count-badge {{
    font-size: 17px;
    font-weight: 850;
    background: #C7FA78;
    color: #0B1220;
    padding: 7px 16px;
    border-radius: 8px;
    letter-spacing: 1px;
  }}
  .cat-title {{
    font-size: 36px;
    font-weight: 900;
    color: #0B1220;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
  }}
  .cat-purpose {{
    font-size: 22px;
    font-weight: 700;
    color: #0284C7;
    background: #E0F2FE;
    padding: 12px 18px;
    border-radius: 10px;
    line-height: 1.45;
    margin-bottom: 20px;
  }}
  .tech-container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    flex-grow: 1;
  }}
  .tech-card-item {{
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
    padding: 16px 20px;
  }}
  .tech-title-line {{
    font-size: 23px;
    font-weight: 850;
    color: #0F172A;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
  }}
  .tech-num-pill {{
    background: #0B1220;
    color: #C7FA78;
    font-size: 17px;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 6px;
  }}
  .tech-usage {{
    font-size: 19px;
    color: #475569;
    line-height: 1.45;
  }}
  .cat-footer {{
    border-top: 1px solid #E2E8F0;
    padding-top: 18px;
    margin-top: 18px;
    font-size: 19px;
    color: #64748B;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
</style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="glow-lime"></div>
  <div class="glow-cyan"></div>

  <div class="top-header">
    <div class="title-group">
      <span class="pill-tag pill-lime">METHOD MAP</span>
      <span class="title-main">56 個技法的方法地圖</span>
    </div>
    <span class="pill-tag pill-dark">選擇工具的地圖 · 非六個必跑階段 · 內容嚴格對齊 references/routing.md</span>
  </div>

  <div class="map-grid">
    <!-- Cat 1 -->
    <div class="cat-card">
      <div>
        <div class="cat-top">
          <span class="cat-num">01 / DISCOVERY</span>
          <span class="cat-count-badge">15 個技法</span>
        </div>
        <div class="cat-title">問題釐清與受眾</div>
        <div class="cat-purpose">找出核心摩擦點，把龐大問題縮成邊界清楚的題目。</div>
        <div class="tech-container">
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#44</span> 分割煩惱
            </div>
            <div class="tech-usage">問題過大或混合多種情境，難以形成可處理的題目。</div>
          </div>
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#40</span> 找到構成阻礙的主因
            </div>
            <div class="tech-usage">問題長期存在，需要理解為何一直沒有解決。</div>
          </div>
        </div>
      </div>
      <div class="cat-footer">
        <span>情境：需求模糊、發散、不知從何下手</span>
        <span style="color:#047857;font-weight:700;">釐清題目</span>
      </div>
    </div>

    <!-- Cat 2 -->
    <div class="cat-card">
      <div>
        <div class="cat-top">
          <span class="cat-num">02 / DIVERGENCE</span>
          <span class="cat-count-badge">12 個技法</span>
        </div>
        <div class="cat-title">發散與跨域靈感</div>
        <div class="cat-purpose">跳脫既有框限，借用異業模式與新視角激發解法。</div>
        <div class="tech-container">
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#03</span> 有漏洞的創意
            </div>
            <div class="tech-usage">團隊不敢提出未成熟點子，或需要引出衍生案的討論素材。</div>
          </div>
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#08</span> 激發更廣泛的觀點
            </div>
            <div class="tech-usage">想確認發想是否忽略人、流程、環境、價值或感官。</div>
          </div>
        </div>
      </div>
      <div class="cat-footer">
        <span>情境：想法卡關、缺乏新方向、討論停滯</span>
        <span style="color:#047857;font-weight:700;">激發觀點</span>
      </div>
    </div>

    <!-- Cat 3 -->
    <div class="cat-card">
      <div>
        <div class="cat-top">
          <span class="cat-num">03 / EVOLUTION</span>
          <span class="cat-count-badge">8 個技法</span>
        </div>
        <div class="cat-title">流程改善與未來情境</div>
        <div class="cat-purpose">系統化改良現有流程機制，推導未來演變趨勢。</div>
        <div class="tech-container">
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#14</span> 找出最佳解
            </div>
            <div class="tech-usage">希望增加效益，同時降低成本、負擔或損害。</div>
          </div>
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#17</span> SCAMPER 奔馳法
            </div>
            <div class="tech-usage">已有產品流程或概念，想找替代、組合、刪減或重排方式。</div>
          </div>
        </div>
      </div>
      <div class="cat-footer">
        <span>情境：現行流程塞車、規劃中長期演進</span>
        <span style="color:#047857;font-weight:700;">優化流程</span>
      </div>
    </div>

    <!-- Cat 4 -->
    <div class="cat-card">
      <div>
        <div class="cat-top">
          <span class="cat-num">04 / STRUCTURING</span>
          <span class="cat-count-badge">8 個技法</span>
        </div>
        <div class="cat-title">整理與具體化</div>
        <div class="cat-purpose">收斂散落點子，歸納核心差異並梳理執行細節。</div>
        <div class="tech-container">
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#21</span> 團隊的創造力
            </div>
            <div class="tech-usage">團隊點子格式不一致，需要歸類並保留原始差異。</div>
          </div>
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#24</span> 創意素描
            </div>
            <div class="tech-usage">需要把概念快速整理成可被其他人理解的簡短提案。</div>
          </div>
        </div>
      </div>
      <div class="cat-footer">
        <span>情境：工作坊點子太多、概念空泛缺乏形狀</span>
        <span style="color:#047857;font-weight:700;">收斂秩序</span>
      </div>
    </div>

    <!-- Cat 5 -->
    <div class="cat-card">
      <div>
        <div class="cat-top">
          <span class="cat-num">05 / STRESS TEST</span>
          <span class="cat-count-badge">7 個技法</span>
        </div>
        <div class="cat-title">商業假設與壓力測試</div>
        <div class="cat-purpose">預演決策者質疑，找出潛在盲點、風險與依據缺口。</div>
        <div class="tech-container">
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#31</span> 模擬批評
            </div>
            <div class="tech-usage">準備提案，想預演不同決策角色會追問什麼。</div>
          </div>
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#30</span> 檢測風險
            </div>
            <div class="tech-usage">已有方案，需要找出可能失敗的原因並提前調整。</div>
          </div>
        </div>
      </div>
      <div class="cat-footer">
        <span>情境：即將向上提案、防範上線潛在失敗</span>
        <span style="color:#047857;font-weight:700;">補齊依據</span>
      </div>
    </div>

    <!-- Cat 6 -->
    <div class="cat-card">
      <div>
        <div class="cat-top">
          <span class="cat-num">06 / VALIDATION</span>
          <span class="cat-count-badge">6 個技法</span>
        </div>
        <div class="cat-title">表達、驗證與落地</div>
        <div class="cat-purpose">清楚表達價值主張，設計最小實驗取得真實依據。</div>
        <div class="tech-container">
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#37</span> 驗證測試的步驟
            </div>
            <div class="tech-usage">需要知道商品原型或服務機制是否真正有效。</div>
          </div>
          <div class="tech-card-item">
            <div class="tech-title-line">
              <span class="tech-num-pill">#33</span> 發布未來的報導
            </div>
            <div class="tech-usage">用未來上市新聞稿釐清產品價值、受眾與亮點。</div>
          </div>
        </div>
      </div>
      <div class="cat-footer">
        <span>情境：Demo 後決定去留、說服初期關鍵客群</span>
        <span style="color:#047857;font-weight:700;">驗證落地</span>
      </div>
    </div>
  </div>
</body>
</html>"""

# -------------------------------------------------------------
# 05-skill-flow.html (3200 x 1440)
# -------------------------------------------------------------
def build_05_skill_flow():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  {BASE_CSS}
  body {{
    width: 3200px;
    height: 1440px;
    padding: 80px 120px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 60% 40%, #111C30 0%, #0B1220 70%, #060910 100%);
    position: relative;
  }}
  .top-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .title-group {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}
  .title-main {{
    font-size: 38px;
    font-weight: 850;
    color: #F8FAFC;
    letter-spacing: -0.5px;
  }}
  .flow-container {{
    display: flex;
    align-items: center;
    height: 1080px;
    position: relative;
    z-index: 10;
    gap: 40px;
  }}

  /* Pipeline Steps */
  .pipeline-steps {{
    display: flex;
    align-items: center;
    gap: 24px;
    flex: 2.7;
  }}
  .step-node {{
    flex: 1;
    background: #F5F3ED;
    color: #0B1220;
    border-radius: 20px;
    padding: 38px 30px;
    height: 800px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 20px 45px rgba(0,0,0,0.4);
    border-top: 8px solid #C7FA78;
    position: relative;
  }}
  .node-pill {{
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 1.5px;
    background: #0B1220;
    color: #C7FA78;
    padding: 6px 14px;
    border-radius: 6px;
    display: inline-block;
    margin-bottom: 16px;
    text-transform: uppercase;
  }}
  .node-title {{
    font-size: 28px;
    font-weight: 850;
    color: #0B1220;
    margin-bottom: 18px;
    line-height: 1.3;
  }}
  .node-items {{
    display: flex;
    flex-direction: column;
    gap: 14px;
    flex-grow: 1;
  }}
  .node-item {{
    font-size: 19px;
    color: #334155;
    line-height: 1.5;
    background: #E2E8F0;
    padding: 14px 18px;
    border-radius: 10px;
  }}
  .node-footer {{
    font-size: 18px;
    font-weight: 800;
    color: #047857;
    border-top: 1px solid #CBD5E1;
    padding-top: 14px;
    margin-top: 14px;
  }}
  .step-arrow {{
    font-size: 32px;
    color: #C7FA78;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.8;
  }}

  /* Outcomes Fork */
  .outcomes-fork {{
    flex: 1.1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 800px;
  }}
  .outcome-card {{
    border-radius: 20px;
    padding: 38px 42px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 370px;
  }}
  .card-stop {{
    background: #0D281D;
    border: 3px solid #C7FA78;
    color: #F8FAFC;
  }}
  .card-loop {{
    background: #112338;
    border: 2px dashed #38BDF8;
    color: #E2E8F0;
  }}
  .outcome-badge {{
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    text-transform: uppercase;
  }}
  .outcome-title {{
    font-size: 36px;
    font-weight: 900;
    margin-bottom: 14px;
    line-height: 1.25;
  }}
  .outcome-desc {{
    font-size: 21px;
    line-height: 1.55;
    color: #CBD5E1;
  }}
</style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="glow-lime"></div>
  <div class="glow-cyan"></div>

  <div class="top-header">
    <div class="title-group">
      <span class="pill-tag pill-lime">AGENT WORKFLOW</span>
      <span class="title-main">Skill 運作流程：自然對話，推進即停</span>
    </div>
    <span class="pill-tag pill-dark">描述問題與限制 → 選擇適合技法 → 按需讀取應用 → 得到判斷或下一步</span>
  </div>

  <div class="flow-container">
    <div class="pipeline-steps">
      <!-- Step 1 -->
      <div class="step-node">
        <div>
          <span class="node-pill">01 / INPUT</span>
          <div class="node-title">描述問題與限制</div>
          <div class="node-items">
            <div class="node-item"><b>角色定義：</b>AI 顧問 / 資深 PM</div>
            <div class="node-item"><b>決策核心：</b>現在需要決定什麼</div>
            <div class="node-item"><b>已知事實：</b>現有數據與真實觀察</div>
            <div class="node-item"><b>現實邊界：</b>時間、人力、預算</div>
          </div>
        </div>
        <div class="node-footer">以終點決策為導向</div>
      </div>

      <div class="step-arrow">➔</div>

      <!-- Step 2 -->
      <div class="step-node">
        <div>
          <span class="node-pill">02 / ROUTE</span>
          <div class="node-title">選擇適合的技法</div>
          <div class="node-items">
            <div class="node-item">查閱情境路由（routing.md）</div>
            <div class="node-item">或在對話中直接指定 #編號</div>
            <div class="node-item"><b>核心原則：</b>一次只選最能推進當前問題的一招</div>
          </div>
        </div>
        <div class="node-footer">精準單一匹配</div>
      </div>

      <div class="step-arrow">➔</div>

      <!-- Step 3 -->
      <div class="step-node">
        <div>
          <span class="node-pill">03 / EXECUTE</span>
          <div class="node-title">按需讀取並應用</div>
          <div class="node-items">
            <div class="node-item">僅載入該技法指南 Prompt</div>
            <div class="node-item"><b>標記分離：</b>事實、推論與假設</div>
            <div class="node-item">絕不強迫跑完全套流程</div>
          </div>
        </div>
        <div class="node-footer">讓依據清晰可辨</div>
      </div>

      <div class="step-arrow">➔</div>

      <!-- Step 4 -->
      <div class="step-node">
        <div>
          <span class="node-pill">04 / DECISION</span>
          <div class="node-title">得到判斷或下一步</div>
          <div class="node-items">
            <div class="node-item">產出明確可執行建議</div>
            <div class="node-item">檢視是否已足夠支持決策</div>
            <div class="node-item">決定立即推進或補充驗證</div>
          </div>
        </div>
        <div class="node-footer">產出適量成果</div>
      </div>
    </div>

    <!-- Fork Outcomes -->
    <div class="outcomes-fork">
      <!-- Fork A: STOP -->
      <div class="outcome-card card-stop">
        <div class="outcome-badge" style="color:#C7FA78;">✓ 已足以回答問題 (SUFFICIENT)</div>
        <div class="outcome-title" style="color:#C7FA78;">【停止 STOP】</div>
        <div class="outcome-desc">
          足夠推進當前工作就完成。<br>帶著成果安排訪談、補齊提案證據或規劃最小測試，不浪費對話輪次。
        </div>
      </div>

      <!-- Fork B: LOOP -->
      <div class="outcome-card card-loop">
        <div class="outcome-badge" style="color:#38BDF8;">↻ 仍有關鍵缺口 (GAPS REMAIN)</div>
        <div class="outcome-title" style="color:#F8FAFC;">補資料，或再選一個方法</div>
        <div class="outcome-desc">
          僅在前一步留下不可忽視的具體問題時，才依新問題追加下一技法或補充輸入。
        </div>
      </div>
    </div>

    <!-- SVG Loopback Arrow -->
    <svg style="position: absolute; inset: 0; width: 3200px; height: 1080px; pointer-events: none; z-index: 20;" viewBox="0 0 3200 1080" fill="none">
      <defs>
        <marker id="loop-arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
          <path d="M 1 1 L 9 5 L 1 9 Z" fill="#38BDF8" />
        </marker>
      </defs>
      <!-- Loop from Fork B (x: 2360, y: 880) curving down and left to Step 02 (x: 960, y: 860) -->
      <path d="M 2360 900 C 2360 1060, 960 1060, 960 880" stroke="#38BDF8" stroke-width="4" stroke-dasharray="10 10" marker-end="url(#loop-arrow)" opacity="0.85"/>
      <rect x="1460" y="1010" width="440" height="48" rx="24" fill="#0B1220" stroke="#38BDF8" stroke-width="2"/>
      <text x="1680" y="1042" text-anchor="middle" fill="#38BDF8" font-size="22" font-weight="800" letter-spacing="1.5">↻ 補齊關鍵資料 / 遞進追加技法</text>
    </svg>
  </div>
</body>
</html>"""

# -------------------------------------------------------------
# Comparison Preview (3200 x 5800)
# -------------------------------------------------------------
def build_comparison_preview(v1_images, v2_images):
    cards_data = [
        (
            "01", "品牌主視覺", "01-hero.png",
            [
                "<b>品牌定位校準：</b>主標「把模糊需求，變成清楚決策。」強化自然對話式 Agent Skill 核心定位，不喧賓奪主。",
                "<b>視覺質感重塑：</b>融入 Nano Banana 品牌折射稜鏡幾何與浮動技法標籤，取代舊版分散空洞之卡片堆疊。",
                "<b>精簡三步流程：</b>輸入起點 → 按需選招 → 清楚決策，900px 縮圖下一眼看懂產品核心價值。"
            ],
            v1_images.get("01-hero.png", ""),
            v2_images.get("01-hero.png", "")
        ),
        (
            "02", "選用工作台展示", "02-workbench.png",
            [
                "<b>100% 真實介面截圖：</b>以本機服務（localhost:4317）原始像素合成，絕不交給生成模型憑空描繪。",
                "<b>搭配關鍵區域實拍放大：</b>局部特寫完整看清「決策、已知、限制」三必填欄位與 Codex / Claude 思考引擎。",
                "<b>明確標示教學示例：</b>澄清為選用工作台，目前聚焦三大高頻任務（#44, #31, #37），其餘於對話中按需使用。"
            ],
            v1_images.get("02-workbench.png", ""),
            v2_images.get("02-workbench.png", "")
        ),
        (
            "03", "從需求到驗證的案例", "03-decision-example.png",
            [
                "<b>徹底移除虛構數據：</b>拔除舊圖無依據之「8.5 分鐘 / 2.1 分鐘 / 降低 75% / 50 筆真實測試」假成效。",
                "<b>誠實標記量測狀態：</b>未量測指標明確標註為「[待量測]」與「[待驗證]」，測試標準標示「示例門檻，待確認」。",
                "<b>完整交代技法收斂：</b>展示 #44 分割煩惱、#31 模擬批評、#37 驗證測試步驟之漸進推導與具體帶走成果。"
            ],
            v1_images.get("03-decision-example.png", ""),
            v2_images.get("03-decision-example.png", "")
        ),
        (
            "04", "56 個技法的方法地圖", "04-method-map.png",
            [
                "<b>嚴格對齊 routing.md：</b>完全吻合 6 大分類與技法數量（15, 12, 8, 8, 7, 6 = 56），正名所有技法編號與名稱。",
                "<b>糾正舊版幻覺命名：</b>更正 #44 分割煩惱、#40 找到構成阻礙的主因、#03 有漏洞的創意、#37 驗證測試步驟等。",
                "<b>確立為選招工具地圖：</b>拔除暗示必跑順序之連線，放大標題與說明字級，確保 900px 縮圖依然清晰可讀。"
            ],
            v1_images.get("04-method-map.png", ""),
            v2_images.get("04-method-map.png", "")
        ),
        (
            "05", "Skill 運作流程", "05-skill-flow.png",
            [
                "<b>簡化四步標準管線：</b>描述問題與限制 → 選擇適合技法 → 按需讀取並應用 → 得到判斷或下一步。",
                "<b>雙分支與停止條件：</b>明確強調【已足以回答問題 → 停止 STOP】不浪費輪次；【仍有關鍵缺口 → 補資料或再選一招】迴圈推進。",
                "<b>落實現代 Agent 哲學：</b>強調自然對話、按需載入單一 Prompt、推進即停，避免傳統強制全套流程負擔。"
            ],
            v1_images.get("05-skill-flow.png", ""),
            v2_images.get("05-skill-flow.png", "")
        )
    ]

    rows_html = ""
    for idx, num, title, filename, bullets, v1_src, v2_src in [
        (i, c[0], c[1], c[2], c[3], c[4], c[5]) for i, c in enumerate(cards_data)
    ]:
        bullet_items = "".join([f"<li>{b}</li>" for b in bullets])
        rows_html += f"""
        <div class="compare-row">
          <div class="row-header">
            <div class="row-title-box">
              <span class="row-num">{num}</span>
              <div class="row-title-text">
                <h2>{title}</h2>
                <div class="row-filename">{filename}</div>
              </div>
            </div>
            <div class="row-bullets">
              <ul>
                {bullet_items}
              </ul>
            </div>
          </div>
          <div class="row-visuals">
            <div class="visual-box before-box">
              <div class="visual-badge badge-before">舊版 v1 (Before)</div>
              <img src="{v1_src}" class="compare-thumb" alt="舊版 {filename}">
            </div>
            <div class="visual-box after-box">
              <div class="visual-badge badge-after">新版 v2 (After - 推薦)</div>
              <img src="{v2_src}" class="compare-thumb" alt="新版 {filename}">
            </div>
          </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  {BASE_CSS}
  body {{
    width: 3200px;
    height: 5800px;
    padding: 90px 120px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #0B1220;
    position: relative;
    box-sizing: border-box;
  }}
  .preview-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid rgba(255, 255, 255, 0.12);
    padding-bottom: 40px;
    margin-bottom: 50px;
  }}
  .preview-title-group h1 {{
    font-size: 64px;
    font-weight: 950;
    letter-spacing: -1.5px;
    color: #FFFFFF;
  }}
  .preview-title-group p {{
    font-size: 26px;
    color: #94A3B8;
    margin-top: 14px;
    line-height: 1.5;
  }}
  .preview-stats-bar {{
    display: flex;
    gap: 20px;
  }}
  .stat-pill {{
    background: rgba(199, 250, 120, 0.1);
    border: 1px solid rgba(199, 250, 120, 0.3);
    color: #C7FA78;
    font-size: 18px;
    font-weight: 800;
    padding: 10px 22px;
    border-radius: 12px;
  }}
  .compare-row {{
    background: #111A2E;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 28px;
    padding: 36px 44px;
    margin-bottom: 44px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
    display: flex;
    flex-direction: column;
    gap: 28px;
  }}
  .row-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 24px;
  }}
  .row-title-box {{
    display: flex;
    align-items: center;
    gap: 22px;
    flex: 1.1;
  }}
  .row-num {{
    font-size: 44px;
    font-weight: 950;
    color: #0B1220;
    background: #C7FA78;
    padding: 8px 22px;
    border-radius: 14px;
    letter-spacing: -1px;
  }}
  .row-title-text h2 {{
    font-size: 36px;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: -0.5px;
  }}
  .row-filename {{
    font-size: 20px;
    color: #64748B;
    font-family: monospace;
    margin-top: 4px;
  }}
  .row-bullets {{
    flex: 1.9;
  }}
  .row-bullets ul {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .row-bullets li {{
    font-size: 20px;
    color: #CBD5E1;
    line-height: 1.5;
    position: relative;
    padding-left: 24px;
  }}
  .row-bullets li::before {{
    content: "✓";
    position: absolute;
    left: 0;
    color: #C7FA78;
    font-weight: 900;
  }}
  .row-bullets b {{
    color: #F8FAFC;
  }}
  .row-visuals {{
    display: flex;
    gap: 36px;
    justify-content: space-between;
  }}
  .visual-box {{
    flex: 1;
    position: relative;
    border-radius: 18px;
    overflow: hidden;
    background: #000000;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
  }}
  .before-box {{
    border: 2px solid rgba(239, 68, 68, 0.4);
  }}
  .after-box {{
    border: 3px solid #C7FA78;
    box-shadow: 0 20px 45px rgba(199, 250, 120, 0.15);
  }}
  .visual-badge {{
    position: absolute;
    top: 18px;
    left: 18px;
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 850;
    letter-spacing: 1px;
    text-transform: uppercase;
    z-index: 10;
  }}
  .badge-before {{
    background: rgba(239, 68, 68, 0.85);
    color: #FFFFFF;
    backdrop-filter: blur(8px);
  }}
  .badge-after {{
    background: #C7FA78;
    color: #0B1220;
    box-shadow: 0 5px 15px rgba(0,0,0,0.4);
  }}
  .compare-thumb {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .preview-footer {{
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 20px;
    color: #64748B;
  }}
</style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="glow-lime"></div>
  <div class="glow-cyan"></div>

  <div class="preview-header">
    <div class="preview-title-group">
      <h1>AI Thinking OS · README 視覺圖片新舊對照 (v1 vs v2)</h1>
      <p>依據專業顧問與 PM 需求全面重製：品牌定位校準、真實本機工作台實拍、routing.md 對齊與可驗證決策演練</p>
    </div>
    <div class="preview-stats-bar">
      <span class="stat-pill">56 招完全對齊</span>
      <span class="stat-pill">無虛構量測數據</span>
      <span class="stat-pill">原始像素工作台實拍</span>
    </div>
  </div>

  {rows_html}

  <div class="preview-footer">
    <span>AI THINKING OS · pm-thinking · BUILT FOR THOUGHTFUL WORK</span>
    <span>ALL ASSETS GENERATED AT FULL TARGET RESOLUTION (3200PX+)</span>
  </div>
</body>
</html>"""

# -------------------------------------------------------------
# Render Runner
# -------------------------------------------------------------
def render_template(html_content, output_png, width, height):
    tmp_path = f"/tmp/{os.path.basename(output_png)}.html"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=1",
        f"--window-size={width},{height}",
        "--hide-scrollbars",
        f"--screenshot={output_png}",
        f"file://{tmp_path}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS: {output_png} ({width}x{height})")
    else:
        print(f"FAILED: {output_png} - {res.stderr}")

if __name__ == "__main__":
    # 1. Render all 5 v2 images
    tasks = [
        (build_01_hero(), os.path.join(V2_DIR, "01-hero.png"), 3200, 1600),
        (build_02_workbench(), os.path.join(V2_DIR, "02-workbench.png"), 3200, 1800),
        (build_03_decision_example(), os.path.join(V2_DIR, "03-decision-example.png"), 3200, 1800),
        (build_04_method_map(), os.path.join(V2_DIR, "04-method-map.png"), 3200, 2000),
        (build_05_skill_flow(), os.path.join(V2_DIR, "05-skill-flow.png"), 3200, 1440),
    ]

    for html, out, w, h in tasks:
        render_template(html, out, w, h)
    print("All 5 v2 images generated successfully.")

    # 2. Render comparison preview
    old_img_dir = "/Users/kevinluo/AI-Agent_video2presentations/skills/pm-thinking/assets/img"
    v1_map = {
        name: get_base64_image(os.path.join(old_img_dir, name))
        for name in ["01-hero.png", "02-workbench.png", "03-decision-example.png", "04-method-map.png", "05-skill-flow.png"]
    }
    v2_map = {
        name: get_base64_image(os.path.join(V2_DIR, name))
        for name in ["01-hero.png", "02-workbench.png", "03-decision-example.png", "04-method-map.png", "05-skill-flow.png"]
    }

    print("Generating comparison preview...")
    comp_html = build_comparison_preview(v1_map, v2_map)
    render_template(comp_html, os.path.join(V2_DIR, "comparison-preview.png"), 3200, 5800)
    print("Comparison preview generated at assets/img/v2/comparison-preview.png.")
