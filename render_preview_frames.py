import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

work_dir = r"C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio\video_work"
os.makedirs(work_dir, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

# Fonts
font_code = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 22)
font_code_bold = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 24)
font_ui = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 24)
font_ui_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
font_small = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)

def create_base_canvas():
    """Dark charcoal to deep navy radial background with subtle ambient lighting"""
    y, x = np.ogrid[:HEIGHT, :WIDTH]
    # Center gradient
    cx, cy = WIDTH / 2, HEIGHT / 2
    dist = np.sqrt((x - cx)**2 + (y - cy)**2) / np.sqrt(cx**2 + cy**2)
    # Background colors: Center is #0B111E (11, 17, 30), edges #05070B (5, 7, 11)
    r = (11 * (1 - dist*0.8)).clip(4, 15)
    g = (17 * (1 - dist*0.75)).clip(6, 20)
    b = (30 * (1 - dist*0.65)).clip(9, 35)
    
    # Add subtle electric blue ambient glow in top-right and cyan in bottom-left
    glow1 = np.exp(-((x - WIDTH*0.7)**2 + (y - HEIGHT*0.3)**2) / (350**2))
    glow2 = np.exp(-((x - WIDTH*0.3)**2 + (y - HEIGHT*0.7)**2) / (400**2))
    
    r += glow1 * 5 + glow2 * 0
    g += glow1 * 25 + glow2 * 20
    b += glow1 * 60 + glow2 * 45
    
    img_data = np.stack([r.clip(0, 255), g.clip(0, 255), b.clip(0, 255)], axis=-1).astype(np.uint8)
    img = Image.fromarray(img_data)
    
    # Add random faint particles
    np.random.seed(42)
    draw = ImageDraw.Draw(img)
    for _ in range(120):
        px = np.random.randint(0, WIDTH)
        py = np.random.randint(0, HEIGHT)
        pr = np.random.uniform(1.0, 2.5)
        pa = np.random.randint(40, 130)
        draw.ellipse([px-pr, py-pr, px+pr, py+pr], fill=(80, 180, 255, pa))
    return img

def render_scene1(t=0.0):
    """Scene 1: Artificial Intelligence & Neural Networks"""
    img = create_base_canvas()
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # 3D Neural Network setup
    layers = [
        # (x_center, [y_nodes], label)
        (WIDTH * 0.28, np.linspace(HEIGHT * 0.25, HEIGHT * 0.75, 5), "Input Layer"),
        (WIDTH * 0.44, np.linspace(HEIGHT * 0.18, HEIGHT * 0.82, 7), "Hidden L1"),
        (WIDTH * 0.60, np.linspace(HEIGHT * 0.18, HEIGHT * 0.82, 7), "Hidden L2"),
        (WIDTH * 0.76, np.linspace(HEIGHT * 0.30, HEIGHT * 0.70, 4), "Output Tensor"),
    ]
    
    # Draw Synaptic Connections with varying glowing alpha
    for l_idx in range(len(layers) - 1):
        x1, y1_list, _ = layers[l_idx]
        x2, y2_list, _ = layers[l_idx + 1]
        for i, y1 in enumerate(y1_list):
            for j, y2 in enumerate(y2_list):
                # Pseudo-random weight & pulse
                weight = math.sin(i * 1.7 + j * 2.3 + l_idx + t*4) * 0.5 + 0.5
                alpha = int(25 + weight * 75)
                # Pulse traveling along wire
                pulse_phase = (t * 2.5 + (i * 3 + j) * 0.15) % 1.0
                px = x1 + (x2 - x1) * pulse_phase
                py = y1 + (y2 - y1) * pulse_phase
                
                # Connection line
                draw.line([(x1, y1), (x2, y2)], fill=(0, 160, 255, alpha), width=1)
                # Glowing pulse
                draw.ellipse([px-2.5, py-2.5, px+2.5, py+2.5], fill=(180, 240, 255, int(alpha * 1.8)))
    
    # Draw Nodes with radial glow
    for l_idx, (x, y_list, label) in enumerate(layers):
        for i, y in enumerate(y_list):
            activation = math.sin(t * 3.0 + l_idx * 1.5 + i) * 0.4 + 0.6
            r_glow = 16 * activation
            r_node = 6 * activation
            # Outer glow
            draw.ellipse([x - r_glow, y - r_glow, x + r_glow, y + r_glow], fill=(0, 200, 255, int(40 * activation)))
            draw.ellipse([x - r_node*1.5, y - r_node*1.5, x + r_node*1.5, y + r_node*1.5], fill=(30, 170, 255, int(120 * activation)))
            # Inner bright core
            draw.ellipse([x - r_node, y - r_node, x + r_node, y + r_node], fill=(220, 245, 255, 255))
        
        # Layer labels
        draw.text((x - 45, HEIGHT * 0.88), label, font=font_small, fill=(0, 200, 255, 180))

    # Floating HUD Tensor Math Annotations
    draw.text((WIDTH * 0.10, HEIGHT * 0.20), "NEURAL ARCHITECTURE // DEEP RESNET", font=font_code_bold, fill=(0, 220, 255, 220))
    draw.text((WIDTH * 0.10, HEIGHT * 0.24), "Loss: 0.00142 | Accuracy: 99.4% | Epoch: 450", font=font_code, fill=(130, 180, 220, 180))
    draw.text((WIDTH * 0.10, HEIGHT * 0.28), "Forward: y = σ(W3 · ReLU(W2 · ReLU(W1·x + b1) + b2) + b3)", font=font_small, fill=(90, 140, 190, 140))
    draw.text((WIDTH * 0.65, HEIGHT * 0.85), "WEIGHT TENSOR: [128, 512, 1024]", font=font_small, fill=(0, 220, 255, 160))
    
    return img

def render_scene2(t=0.0):
    """Scene 2: Modern Web Development"""
    img = create_base_canvas()
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # 3D Perspective Floating Browser Window (Simulated with skewed/offset layers)
    bx, by, bw, bh = WIDTH * 0.12, HEIGHT * 0.18, WIDTH * 0.76, HEIGHT * 0.68
    
    # Window glow & drop shadow
    draw.rectangle([bx-10, by-10, bx+bw+10, by+bh+10], fill=(0, 100, 200, 25))
    draw.rectangle([bx, by, bx+bw, by+bh], fill=(12, 16, 26, 230), outline=(0, 160, 240, 140), width=2)
    
    # Title bar
    draw.rectangle([bx, by, bx+bw, by+44], fill=(18, 24, 38, 240), outline=(0, 160, 240, 80), width=1)
    # Window controls (macOS style sleek dots)
    draw.ellipse([bx+16, by+15, bx+28, by+27], fill=(255, 95, 87, 220))
    draw.ellipse([bx+36, by+15, bx+48, by+27], fill=(254, 188, 46, 220))
    draw.ellipse([bx+56, by+15, bx+68, by+27], fill=(40, 200, 64, 220))
    # URL bar
    draw.rectangle([bx+100, by+10, bx+bw-120, by+34], fill=(10, 14, 22, 220), outline=(0, 140, 220, 60), width=1)
    draw.text((bx+120, by+14), "https://nithin-r.dev/dashboard/ai-vision", font=font_small, fill=(100, 180, 240, 200))
    
    # Left Pane: Code Editor (VS Code / Sublime aesthetic)
    cx, cy, cw, ch = bx+20, by+64, bw*0.48, bh-84
    draw.rectangle([cx, cy, cx+cw, cy+ch], fill=(8, 12, 20, 220), outline=(30, 60, 90, 140))
    draw.rectangle([cx, cy, cx+cw, cy+32], fill=(15, 20, 32, 240))
    draw.text((cx+16, cy+8), "App.tsx  •  Interactive Web Client", font=font_small, fill=(0, 210, 255, 220))
    
    code_lines = [
        ("import React, { useState, useEffect } from 'react';", (180, 140, 255)),
        ("import { NeuralEngine, Predictor } from '@core/ai';", (0, 220, 255)),
        ("", (255, 255, 255)),
        ("export const VisionModel = ({ dataset }) => {", (255, 180, 60)),
        ("  const [inference, setInference] = useState(null);", (120, 220, 255)),
        ("  useEffect(() => {", (255, 120, 180)),
        ("    const engine = new NeuralEngine({ workers: 4 });", (200, 220, 240)),
        ("    engine.streamPredictions((data) => {", (120, 220, 255)),
        ("      setInference({ ...data, latency: '4.2ms' });", (150, 255, 150)),
        ("    });", (120, 220, 255)),
        ("  }, [dataset]);", (255, 120, 180)),
        ("  return <DashboardLayout live={inference} />;", (0, 230, 255)),
        ("};", (255, 180, 60)),
    ]
    for idx, (code, col) in enumerate(code_lines):
        draw.text((cx+16, cy + 44 + idx*23), f"{idx+1:2d}  {code}", font=font_small, fill=(col[0], col[1], col[2], 230))
    
    # Right Pane: Interactive Rendered UI
    rx, ry, rw, rh = cx+cw+20, cy, bw*0.46 - 20, ch
    draw.rectangle([rx, ry, rx+rw, ry+rh], fill=(10, 15, 24, 220), outline=(0, 140, 220, 100))
    draw.rectangle([rx, ry, rx+rw, ry+32], fill=(16, 24, 38, 240))
    draw.text((rx+16, ry+8), "PREVIEW // Responsive UI Grid", font=font_small, fill=(0, 220, 255, 200))
    
    # UI Card 1
    draw.rectangle([rx+16, ry+48, rx+rw-16, ry+140], fill=(18, 26, 42, 220), outline=(0, 180, 255, 140))
    draw.text((rx+30, ry+60), "Real-Time AI Inference", font=font_ui_bold, fill=(240, 250, 255, 255))
    draw.text((rx+30, ry+96), "99.8% Accuracy  |  4.2ms Latency  |  Active Streams: 32", font=font_small, fill=(0, 220, 255, 200))
    
    # Animated Line Graph Widget
    gx, gy, gw, gh = rx+16, ry+156, rw-32, 130
    draw.rectangle([gx, gy, gx+gw, gy+gh], fill=(14, 20, 32, 220), outline=(30, 60, 90, 140))
    # Draw graph grid lines
    for ly in range(3):
        draw.line([(gx+10, gy+30+ly*35), (gx+gw-10, gy+30+ly*35)], fill=(30, 50, 75, 100))
    # Plot line
    points = []
    for step in range(12):
        px = gx + 15 + step * (gw - 30) / 11
        py = gy + gh - 25 - math.sin(step * 0.6 + t*3) * 35 - math.cos(step * 1.2) * 20
        points.append((px, py))
    draw.line(points, fill=(0, 240, 255, 240), width=2)
    for px, py in points:
        draw.ellipse([px-3, py-3, px+3, py+3], fill=(220, 250, 255, 255))

    return img

def render_scene3(t=0.0):
    """Scene 3: Mobile App Development & Cross-Platform"""
    img = create_base_canvas()
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Centered floating modern smartphone mockup
    pw, ph = 420, 780
    px = WIDTH / 2 - pw / 2
    py = HEIGHT / 2 - ph / 2 + 20
    
    # Outer phone shadow & neon rim glow
    draw.rounded_rectangle([px-12, py-12, px+pw+12, py+ph+12], radius=56, fill=(0, 140, 255, 30))
    # Phone Body (dark metallic titanium)
    draw.rounded_rectangle([px-4, py-4, px+pw+4, py+ph+4], radius=50, fill=(25, 30, 42, 255), outline=(0, 180, 255, 160), width=2)
    # Screen Area
    sx, sy, sw, sh = px+12, py+14, pw-24, ph-28
    draw.rounded_rectangle([sx, sy, sx+sw, sy+sh], radius=40, fill=(8, 11, 18, 255))
    
    # Dynamic Island / Notch
    draw.rounded_rectangle([sx+sw/2-55, sy+12, sx+sw/2+55, sy+38], radius=13, fill=(0, 0, 0, 255), outline=(30, 40, 60, 160))
    draw.ellipse([sx+sw/2+32, sy+20, sx+sw/2+42, sy+30], fill=(0, 180, 255, 180)) # Camera lens
    
    # Mobile App UI Header
    draw.text((sx+24, sy+56), "AI Neural Scanner", font=font_ui_bold, fill=(240, 250, 255, 255))
    draw.text((sx+24, sy+90), "CROSS-PLATFORM REACT NATIVE / FLUTTER", font=font_small, fill=(0, 210, 255, 200))
    
    # Main Mobile Card (Visual Recognition UI)
    cx, cy, cw, ch = sx+20, sy+125, sw-40, 310
    draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=20, fill=(16, 22, 35, 240), outline=(0, 160, 240, 140))
    
    # Holographic camera scan frame inside card
    fx, fy, fw, fh = cx+20, cy+20, cw-40, 200
    draw.rounded_rectangle([fx, fy, fx+fw, fy+fh], radius=14, fill=(10, 14, 24, 255), outline=(0, 220, 255, 100))
    # Corner scan reticles
    for ox, oy in [(fx+10, fy+10), (fx+fw-25, fy+10), (fx+10, fy+fh-25), (fx+fw-25, fy+fh-25)]:
        draw.rectangle([ox, oy, ox+15, oy+15], outline=(0, 240, 255, 240), width=2)
    # Animated Scan line
    scan_y = fy + 15 + ((t * 80) % (fh - 30))
    draw.line([(fx+15, scan_y), (fx+fw-15, scan_y)], fill=(0, 240, 255, 200), width=2)
    draw.text((fx+25, fy+fh-35), "CLASSIFICATION: DETECTED (98.9%)", font=font_small, fill=(0, 240, 255, 230))
    
    draw.text((cx+20, cy+240), "Target: Multimodal LLM Agent", font=font_code, fill=(220, 240, 255, 255))
    draw.text((cx+20, cy+270), "Inference latency: 12ms (DirectML / CoreML)", font=font_small, fill=(100, 180, 240, 180))

    # Bottom Mobile Nav Bar
    draw.rounded_rectangle([sx+16, sy+sh-70, sx+sw-16, sy+sh-16], radius=25, fill=(14, 20, 32, 240), outline=(30, 60, 90, 140))
    nav_labels = ["Home", "Models", "Sensors", "Profile"]
    for i, lbl in enumerate(nav_labels):
        nx = sx + 30 + i * (sw - 60) / 3.5
        col = (0, 240, 255) if i == 1 else (100, 140, 180)
        draw.text((nx, sy+sh-50), lbl, font=font_small, fill=(col[0], col[1], col[2], 220))

    # Side annotations for cross-platform ecosystem
    draw.text((WIDTH * 0.10, HEIGHT * 0.40), "CROSS-PLATFORM ARCHITECTURE", font=font_title, fill=(0, 220, 255, 220))
    draw.text((WIDTH * 0.10, HEIGHT * 0.47), "• iOS & Android Native Core\n• On-Device Neural Engine\n• 60 FPS Fluid Gesture Engine\n• Offline ML Inference", font=font_code, fill=(160, 200, 240, 190))
    
    return img

def render_scene4(t=0.0):
    """Scene 4: Software Engineering & Systems Architecture"""
    img = create_base_canvas()
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Left Side: High Performance Backend Python & API Code
    cx, cy, cw, ch = WIDTH * 0.08, HEIGHT * 0.20, WIDTH * 0.42, HEIGHT * 0.62
    draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=16, fill=(10, 14, 22, 230), outline=(0, 160, 240, 120), width=2)
    # Header
    draw.rectangle([cx, cy, cx+cw, cy+36], fill=(16, 22, 34, 240))
    draw.text((cx+20, cy+8), "pipeline_service.py  (Python 3.12 / Flask / Torch)", font=font_small, fill=(0, 220, 255, 220))
    
    py_code = [
        ("from flask import Flask, request, jsonify", (255, 140, 100)),
        ("import torch, redis, asyncio", (255, 140, 100)),
        ("from architecture.cluster import DistributedNodes", (0, 220, 255)),
        ("", (255, 255, 255)),
        ("@app.route('/v1/system/cluster', methods=['POST'])", (255, 200, 60)),
        ("async def dispatch_workload():", (120, 220, 255)),
        ("    payload = request.get_json()", (220, 230, 245)),
        ("    cache_key = f'cache:{hash(payload)}'", (150, 255, 150)),
        ("    if result := redis_client.get(cache_key):", (255, 120, 180)),
        ("        return jsonify({'cached': True, 'data': result})", (150, 255, 150)),
        ("    # Parallel Distributed Matrix Compute", (90, 140, 190)),
        ("    tensors = torch.tensor(payload['features'])", (220, 230, 245)),
        ("    output = await model_cluster.infer(tensors)", (0, 240, 255)),
        ("    return jsonify({'status': 200, 'res': output})", (150, 255, 150)),
    ]
    for idx, (code, col) in enumerate(py_code):
        draw.text((cx+18, cy + 50 + idx*24), f"{idx+1:2d}  {code}", font=font_small, fill=(col[0], col[1], col[2], 230))
        
    # Right Side: Distributed Microservices Architecture Diagram
    dx, dy, dw, dh = WIDTH * 0.54, HEIGHT * 0.20, WIDTH * 0.38, HEIGHT * 0.62
    draw.rounded_rectangle([dx, dy, dx+dw, dy+dh], radius=16, fill=(10, 14, 24, 230), outline=(0, 140, 220, 100))
    draw.rectangle([dx, dy, dx+dw, dy+36], fill=(16, 22, 34, 240))
    draw.text((dx+20, dy+8), "DISTRIBUTED BACKEND ARCHITECTURE", font=font_small, fill=(0, 220, 255, 220))
    
    # Diagram Nodes: Client -> Gateway -> Services -> Database
    nodes = [
        (dx + dw*0.5, dy + 80, "CLIENT / EDGE CLIENTS", (0, 200, 255)),
        (dx + dw*0.5, dy + 180, "API GATEWAY & LOAD BALANCER", (60, 220, 200)),
        (dx + dw*0.28, dy + 290, "AI INFERENCE WORKER", (180, 140, 255)),
        (dx + dw*0.72, dy + 290, "DATA PIPELINE SERVICE", (255, 180, 80)),
        (dx + dw*0.5, dy + 410, "POSTGRESQL & REDIS CLUSTER", (80, 220, 140)),
    ]
    
    # Draw data pathways
    for n1, n2 in [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)]:
        x1, y1, _, _ = nodes[n1]
        x2, y2, _, _ = nodes[n2]
        draw.line([(x1, y1), (x2, y2)], fill=(0, 140, 220, 140), width=2)
        # Animated packet pulse
        pulse = (t * 2.0 + n1 * 0.4) % 1.0
        ppx = x1 + (x2 - x1) * pulse
        ppy = y1 + (y2 - y1) * pulse
        draw.ellipse([ppx-4, ppy-4, ppx+4, ppy+4], fill=(220, 255, 255, 255))
        
    for x, y, label, col in nodes:
        draw.rounded_rectangle([x-110, y-20, x+110, y+20], radius=10, fill=(16, 24, 38, 255), outline=col, width=2)
        draw.text((x-90, y-10), label, font=font_small, fill=(col[0], col[1], col[2], 240))

    return img

def render_scene5(t=0.0):
    """Scene 5: Unified Technology Nexus (All 4 Disciplines Converged)"""
    img = create_base_canvas()
    draw = ImageDraw.Draw(img, 'RGBA')
    
    cx, cy = WIDTH / 2, HEIGHT / 2
    
    # Central Pulsating Technology Core
    r_core = 70 + math.sin(t * 3.0) * 8
    # Outer core halos
    for radius, alpha in [(r_core * 2.2, 20), (r_core * 1.6, 50), (r_core * 1.2, 120)]:
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=(0, 160, 255, alpha))
    draw.ellipse([cx-r_core, cy-r_core, cx+r_core, cy+r_core], fill=(180, 235, 255, 255), outline=(0, 240, 255, 255), width=3)
    
    # Orbiting Disciplines at 4 quadrants
    quadrants = [
        (cx - 380, cy - 180, "ARTIFICIAL INTELLIGENCE & ML", "Neural Nets • PyTorch • Deep Learning", (0, 230, 255)),
        (cx + 380, cy - 180, "MODERN WEB DEVELOPMENT", "Full-Stack • React • Responsive UI", (0, 200, 255)),
        (cx - 380, cy + 180, "MOBILE APP DEVELOPMENT", "Cross-Platform • iOS • Android Native", (100, 220, 255)),
        (cx + 380, cy + 180, "SOFTWARE ENGINEERING", "Distributed Systems • Python • APIs", (140, 200, 255)),
    ]
    
    # Connecting Energy Conduits
    for qx, qy, title, subtitle, col in quadrants:
        # Curved or segmented conduit
        draw.line([(cx, cy), (qx, qy)], fill=(0, 160, 240, 160), width=2)
        # Pulse
        pulse = (t * 2.0 + (qx + qy)*0.001) % 1.0
        px = cx + (qx - cx) * pulse
        py = cy + (qy - cy) * pulse
        draw.ellipse([px-5, py-5, px+5, py+5], fill=(220, 255, 255, 255))
        
        # Quadrant Box
        draw.rounded_rectangle([qx-180, qy-45, qx+180, qy+45], radius=14, fill=(12, 18, 30, 230), outline=col, width=2)
        draw.text((qx-160, qy-30), title, font=font_code_bold, fill=(col[0], col[1], col[2], 255))
        draw.text((qx-160, qy+5), subtitle, font=font_small, fill=(180, 210, 240, 180))

    # Center Title
    draw.text((cx - 100, cy - 12), "INTELLIGENCE", font=font_small, fill=(10, 20, 40, 255))
    
    return img

print("Rendering scene previews...")
render_scene1().save(os.path.join(work_dir, "preview_scene1.jpg"), quality=92)
print("Saved Scene 1")
render_scene2().save(os.path.join(work_dir, "preview_scene2.jpg"), quality=92)
print("Saved Scene 2")
render_scene3().save(os.path.join(work_dir, "preview_scene3.jpg"), quality=92)
print("Saved Scene 3")
render_scene4().save(os.path.join(work_dir, "preview_scene4.jpg"), quality=92)
print("Saved Scene 4")
render_scene5().save(os.path.join(work_dir, "preview_scene5.jpg"), quality=92)
print("Saved Scene 5")
print("All 5 previews rendered successfully!")
