import os
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio\static\images\projects"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1200, 800

# Try to get Windows fonts
try:
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 46)
    font_subtitle = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 22)
    font_tag = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)
    font_metric = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 36)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 14)
except Exception:
    font_title = font_subtitle = font_tag = font_metric = font_small = ImageFont.load_default()

def create_base(bg_color=(10, 10, 12), border_color=(35, 35, 42)):
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    # Background subtle grid
    grid_size = 40
    for x in range(0, W, grid_size):
        draw.line([(x, 0), (x, H)], fill=(18, 18, 22), width=1)
    for y in range(0, H, grid_size):
        draw.line([(0, y), (W, y)], fill=(18, 18, 22), width=1)
    # Outer frame
    draw.rectangle([30, 30, W - 30, H - 30], outline=border_color, width=2)
    # Header bar
    draw.line([(30, 90), (W - 30, 90)], fill=border_color, width=1)
    # Top status
    draw.ellipse([50, 56, 62, 68], fill=(235, 235, 240))
    return img, draw

# 1. AGENTGUARD AI
def gen_agentguard():
    img, draw = create_base((8, 10, 15), (28, 38, 55))
    draw.text((75, 54), "AGENTGUARD AI // RUNTIME AGENT SECURITY GATEWAY", fill=(160, 175, 195), font=font_small)
    draw.text((W - 220, 54), "VERSION 2.4.0  •  LIVE", fill=(0, 240, 255), font=font_small)
    
    # Title
    draw.text((60, 130), "AGENTGUARD AI", fill=(255, 255, 255), font=font_title)
    draw.text((60, 190), "Autonomous Multi-Agent Security, Prompt Firewall & Tool Guardrails", fill=(140, 160, 185), font=font_subtitle)
    
    # Architecture Diagram Center
    box_y = 260
    # Left Box: Agent Workflow
    draw.rectangle([60, box_y, 350, box_y + 360], outline=(40, 60, 90), fill=(12, 16, 26), width=2)
    draw.text((80, box_y + 20), "AGENT RUNTIME", fill=(255, 255, 255), font=font_subtitle)
    draw.text((80, box_y + 60), "• Tool Dispatcher\n• LLM Orchestration\n• Memory Context\n• Subagent Mesh", fill=(140, 160, 190), font=font_tag)
    
    # Middle Box: Security Proxy Core
    draw.rectangle([430, box_y - 20, 770, box_y + 380], outline=(0, 220, 240), fill=(15, 24, 38), width=2)
    draw.text((455, box_y + 10), "SECURITY GATEWAY CORE", fill=(0, 240, 255), font=font_subtitle)
    draw.line([(455, box_y + 45), (745, box_y + 45)], fill=(0, 220, 240), width=1)
    draw.text((455, box_y + 70), "• Prompt Injection Firewall\n• Privilege Escalation Filter\n• Zero-Trust Policy Engine\n• Anomaly Vector Detection\n• Tool Calling Guardrail", fill=(220, 235, 255), font=font_tag)
    
    # Metrics in core
    draw.rectangle([455, box_y + 250, 745, box_y + 350], outline=(30, 80, 110), fill=(8, 15, 25))
    draw.text((475, box_y + 265), "THREAT INTERCEPTION RATE", fill=(120, 160, 190), font=font_small)
    draw.text((475, box_y + 295), "99.84%", fill=(0, 255, 180), font=font_metric)
    
    # Right Box: Target Systems
    draw.rectangle([850, box_y, 1140, box_y + 360], outline=(40, 60, 90), fill=(12, 16, 26), width=2)
    draw.text((870, box_y + 20), "SECURED ENVIRONMENTS", fill=(255, 255, 255), font=font_subtitle)
    draw.text((870, box_y + 60), "• Production APIs\n• SQL / Vector Databases\n• Bash / Execution Sandboxes\n• SaaS Webhooks", fill=(140, 160, 190), font=font_tag)
    
    # Connecting Arrows
    draw.line([(350, box_y + 160), (430, box_y + 160)], fill=(0, 240, 255), width=3)
    draw.line([(770, box_y + 160), (850, box_y + 160)], fill=(0, 240, 255), width=3)
    
    # Footer badges
    draw.text((60, 710), "STACK: PYTHON  •  FASTAPI  •  PYTORCH  •  LLM GUARDRAILS  •  REACT", fill=(100, 120, 150), font=font_small)
    img.save(os.path.join(OUTPUT_DIR, "agentguard.png"), quality=95)

# 2. STUDENT MENTAL HEALTH
def gen_mental_health():
    img, draw = create_base((12, 10, 10), (50, 30, 30))
    draw.text((75, 54), "CLINICAL AI // STUDENT MENTAL HEALTH & DEPRESSION SYSTEM", fill=(190, 160, 160), font=font_small)
    draw.text((W - 250, 54), "DIAGNOSTIC PROTOCOL: PHQ-9", fill=(255, 120, 120), font=font_small)
    
    draw.text((60, 130), "STUDENT MENTAL HEALTH PLATFORM", fill=(255, 255, 255), font=font_title)
    draw.text((60, 190), "Clinical Depression Screening, NLP Affect Detection & Care Pathways", fill=(190, 160, 160), font=font_subtitle)
    
    box_y = 260
    # Left Card: Psychometric Scoring
    draw.rectangle([60, box_y, 570, box_y + 380], outline=(70, 35, 35), fill=(20, 14, 14), width=2)
    draw.text((90, box_y + 30), "PSYCHOMETRIC FEATURE MATRIX", fill=(255, 200, 200), font=font_subtitle)
    draw.text((90, box_y + 80), "• PHQ-9 Depression Severity Index\n• GAD-7 Anxiety Assessment Scales\n• Longitudinal Mood Tracking\n• Sleep Disturbance & Academic Stress Correlations", fill=(180, 150, 150), font=font_tag)
    
    # Progress bars
    scores = [("PHQ-9 Composite", 0.72), ("Academic Pressure", 0.85), ("Social Isolation", 0.60)]
    sy = box_y + 220
    for label, val in scores:
        draw.text((90, sy), label, fill=(160, 130, 130), font=font_small)
        draw.rectangle([90, sy + 22, 540, sy + 32], outline=(60, 35, 35), fill=(30, 18, 18))
        draw.rectangle([90, sy + 22, 90 + int(450 * val), sy + 32], fill=(240, 80, 80))
        sy += 50

    # Right Card: ML Ensemble & Risk Stratification
    draw.rectangle([630, box_y, 1140, box_y + 380], outline=(70, 35, 35), fill=(20, 14, 14), width=2)
    draw.text((660, box_y + 30), "ML ENSEMBLE CLASSIFICATION", fill=(255, 200, 200), font=font_subtitle)
    draw.text((660, box_y + 80), "• Random Forest & Support Vector Machines\n• Sentiment Analysis on Free-text Reflections\n• Multi-Class Severity Triage (Mild / Moderate / Severe)\n• Privacy-Preserving Encryption Protocol", fill=(180, 150, 150), font=font_tag)
    
    draw.rectangle([660, box_y + 240, 1110, box_y + 340], outline=(90, 40, 40), fill=(28, 16, 16))
    draw.text((680, box_y + 255), "CROSS-VALIDATION CLASSIFICATION F1", fill=(200, 140, 140), font=font_small)
    draw.text((680, box_y + 285), "92.6% F1-SCORE", fill=(255, 100, 100), font=font_metric)

    draw.text((60, 710), "STACK: PYTHON  •  SCIKIT-LEARN  •  FLASK  •  SQLITE  •  PANDAS", fill=(140, 110, 110), font=font_small)
    img.save(os.path.join(OUTPUT_DIR, "mental_health.png"), quality=95)

# 3. AI FINANCE CONTROLLER
def gen_ai_finance():
    img, draw = create_base((10, 12, 10), (30, 50, 35))
    draw.text((75, 54), "FINANCIAL INTELLIGENCE // AUTONOMOUS EXPENSE & CAPITAL SYSTEM", fill=(150, 190, 160), font=font_small)
    draw.text((W - 250, 54), "SYSTEM STATUS: MONITORING", fill=(80, 255, 160), font=font_small)
    
    draw.text((60, 130), "AI FINANCE CONTROLLER", fill=(255, 255, 255), font=font_title)
    draw.text((60, 190), "Algorithmic Cash Flow Forecasting, Spend Anomaly Detection & Planning", fill=(150, 190, 160), font=font_subtitle)
    
    box_y = 260
    # Left Card: Time-series curve
    draw.rectangle([60, box_y, 680, box_y + 380], outline=(35, 75, 45), fill=(12, 22, 15), width=2)
    draw.text((90, box_y + 25), "PREDICTIVE CASH FLOW TRAJECTORY", fill=(200, 255, 220), font=font_subtitle)
    
    # Draw graph grid
    gx0, gy0, gx1, gy1 = 90, box_y + 80, 650, box_y + 340
    draw.rectangle([gx0, gy0, gx1, gy1], outline=(25, 50, 30), fill=(8, 16, 10))
    for gy in range(gy0, gy1, 50):
        draw.line([(gx0, gy), (gx1, gy)], fill=(18, 35, 22), width=1)
    for gx in range(gx0, gx1, 80):
        draw.line([(gx, gy0), (gx, gy1)], fill=(18, 35, 22), width=1)
        
    # Draw forecast spline
    pts = [(gx0, gy1 - 60), (gx0 + 80, gy1 - 100), (gx0 + 160, gy1 - 70), (gx0 + 240, gy1 - 150),
           (gx0 + 320, gy1 - 130), (gx0 + 400, gy1 - 190), (gx0 + 480, gy1 - 170), (gx1, gy1 - 230)]
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=(60, 255, 140), width=3)
    for p in pts:
        draw.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill=(255, 255, 255))
        
    # Right Card: Anomaly & Metrics
    draw.rectangle([720, box_y, 1140, box_y + 380], outline=(35, 75, 45), fill=(12, 22, 15), width=2)
    draw.text((750, box_y + 25), "ANOMALY DETECTION ENGINE", fill=(200, 255, 220), font=font_subtitle)
    draw.text((750, box_y + 70), "• Isolation Forest Anomaly Filter\n• Recurring Expense Fingerprinting\n• Rolling Liquidity Projections\n• Automated Variance Alerts", fill=(160, 200, 170), font=font_tag)
    
    draw.rectangle([750, box_y + 220, 1110, box_y + 340], outline=(40, 90, 55), fill=(15, 30, 20))
    draw.text((770, box_y + 235), "PROJECTED SAVINGS OPTIMIZATION", fill=(140, 190, 150), font=font_small)
    draw.text((770, box_y + 270), "+28.4% APY GAIN", fill=(60, 255, 140), font=font_metric)
    
    draw.text((60, 710), "STACK: PYTHON  •  NUMPY  •  SCIKIT-LEARN  •  FLASK  •  CHART.JS", fill=(120, 150, 130), font=font_small)
    img.save(os.path.join(OUTPUT_DIR, "ai_finance.png"), quality=95)

# 4. FULL-STACK PERSONAL PORTFOLIO
def gen_portfolio_showcase():
    img, draw = create_base((12, 12, 14), (45, 45, 52))
    draw.text((75, 54), "PORTFOLIO ARCHITECTURE // SWISS MINIMALIST EDITORIAL PLATFORM", fill=(180, 180, 190), font=font_small)
    draw.text((W - 250, 54), "DESIGN SYSTEM: DENNY PRATAMA", fill=(240, 240, 245), font=font_small)
    
    draw.text((60, 130), "SWISS EDITORIAL PORTFOLIO", fill=(255, 255, 255), font=font_title)
    draw.text((60, 190), "Three.js 3D Architectural Centerpiece, High-Contrast Typography & Flask", fill=(180, 180, 190), font=font_subtitle)
    
    box_y = 260
    # Left Card: Wireframe 3D Sphere / Lattice
    draw.rectangle([60, box_y, 560, box_y + 380], outline=(60, 60, 70), fill=(18, 18, 22), width=2)
    draw.text((90, box_y + 25), "INTERACTIVE 3D COMPUTING CORE", fill=(255, 255, 255), font=font_subtitle)
    # Draw geometric icosahedron lines
    cx, cy = 310, box_y + 220
    r = 110
    n = 8
    poly_pts = []
    for i in range(n):
        ang = i * (2 * math.pi / n)
        poly_pts.append((cx + int(r * math.cos(ang)), cy + int(r * math.sin(ang) * 0.7)))
    for i in range(n):
        for j in range(i+1, n):
            draw.line([poly_pts[i], poly_pts[j]], fill=(100, 100, 120), width=1)
    for p in poly_pts:
        draw.ellipse([p[0]-5, p[1]-5, p[0]+5, p[1]+5], fill=(255, 255, 255))
        
    # Right Card: Full-Stack Specifications
    draw.rectangle([600, box_y, 1140, box_y + 380], outline=(60, 60, 70), fill=(18, 18, 22), width=2)
    draw.text((630, box_y + 25), "FULL-STACK CAPABILITIES", fill=(255, 255, 255), font=font_subtitle)
    draw.text((630, box_y + 70), "• Python Flask Microservices Architecture\n• SQLite Storage with CSRF Protection\n• Google Sheets & SMTP Notification Pipeline\n• Swiss Asymmetric Layouts & GSAP Motion\n• Ultra-Fast Sub-50ms SSR & Client Interactions", fill=(200, 200, 215), font=font_tag)
    
    draw.rectangle([630, box_y + 230, 1100, box_y + 340], outline=(80, 80, 95), fill=(24, 24, 30))
    draw.text((650, box_y + 245), "LIGHTHOUSE AUDIT SCORES", fill=(170, 170, 180), font=font_small)
    draw.text((650, box_y + 275), "100 / 100 / 100 / 100", fill=(255, 255, 255), font=font_metric)

    draw.text((60, 710), "STACK: PYTHON  •  FLASK  •  THREE.JS  •  SQLITE  •  GSAP  •  JINJA2", fill=(140, 140, 155), font=font_small)
    img.save(os.path.join(OUTPUT_DIR, "portfolio_showcase.png"), quality=95)

# 5. MACHINE LEARNING RESEARCH & PREDICTION SUITE
def gen_ml_suite():
    img, draw = create_base((12, 10, 14), (45, 35, 55))
    draw.text((75, 54), "APPLIED AI // PREDICTIVE MODELING & NLP BENCHMARK SUITE", fill=(180, 160, 190), font=font_small)
    draw.text((W - 250, 54), "TEST ACCURACY: 94.0%", fill=(220, 140, 255), font=font_small)
    
    draw.text((60, 130), "ML PREDICTION & RESEARCH SUITE", fill=(255, 255, 255), font=font_title)
    draw.text((60, 190), "Disease Risk Classification & Transformer-Based Sentiment Pipeline", fill=(180, 160, 190), font=font_subtitle)
    
    box_y = 260
    # Left Card: Disease Risk
    draw.rectangle([60, box_y, 570, box_y + 380], outline=(65, 45, 80), fill=(20, 15, 25), width=2)
    draw.text((90, box_y + 25), "DISEASE PREDICTION CLASSIFIER", fill=(230, 200, 255), font=font_subtitle)
    draw.text((90, box_y + 70), "• Multi-Symptom Diagnostic Feature Tree\n• Random Forest & Support Vector Machines\n• Hyperparameter Optimization via GridSearch\n• 94% Validation Accuracy on Test Cohort", fill=(190, 170, 210), font=font_tag)
    
    draw.rectangle([90, box_y + 230, 530, box_y + 340], outline=(85, 55, 105), fill=(28, 20, 35))
    draw.text((110, box_y + 245), "DIAGNOSTIC TEST ACCURACY", fill=(180, 150, 200), font=font_small)
    draw.text((110, box_y + 275), "94.2% ACCURACY", fill=(210, 120, 255), font=font_metric)
    
    # Right Card: NLP Sentiment
    draw.rectangle([610, box_y, 1140, box_y + 380], outline=(65, 45, 80), fill=(20, 15, 25), width=2)
    draw.text((640, box_y + 25), "TRANSFORMER NLP SENTIMENT", fill=(230, 200, 255), font=font_subtitle)
    draw.text((640, box_y + 70), "• Fine-Tuned BERT Sequence Classification\n• Lexicon-Augmented VADER Baseline Analysis\n• Real-Time Polarity Score Decomposition\n• High-Throughput Batch Inference", fill=(190, 170, 210), font=font_tag)
    
    draw.rectangle([640, box_y + 230, 1100, box_y + 340], outline=(85, 55, 105), fill=(28, 20, 35))
    draw.text((660, box_y + 245), "TOKEN THROUGHPUT / LATENCY", fill=(180, 150, 200), font=font_small)
    draw.text((660, box_y + 275), "18ms / INFERENCE", fill=(210, 120, 255), font=font_metric)

    draw.text((60, 710), "STACK: PYTHON  •  SCIKIT-LEARN  •  TRANSFORMERS  •  BERT  •  PANDAS", fill=(150, 130, 160), font=font_small)
    img.save(os.path.join(OUTPUT_DIR, "ml_suite.png"), quality=95)

if __name__ == "__main__":
    gen_agentguard()
    gen_mental_health()
    gen_ai_finance()
    gen_portfolio_showcase()
    gen_ml_suite()
    print("All 5 project preview images generated successfully.")
