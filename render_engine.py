import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

WIDTH, HEIGHT = 1920, 1080
CX, CY = WIDTH / 2, HEIGHT / 2
FPS = 30
TOTAL_DURATION = 15.0
TOTAL_FRAMES = int(FPS * TOTAL_DURATION)

# High Quality Typography
font_code = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 20)
font_code_bold = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 23)
font_code_small = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 15)
font_code_tiny = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 13)
font_ui = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)
font_ui_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)

# Precomputed Static Background Grid & Subtle Vignette
y, x = np.ogrid[:HEIGHT, :WIDTH]
dist = np.sqrt((x - CX)**2 + (y - CY)**2) / np.sqrt(CX**2 + CY**2)

# Midnight navy with subtle cyan ambient floor
base_r = (10 * (1 - dist*0.6)).clip(4, 16).astype(np.float32)
base_g = (16 * (1 - dist*0.5)).clip(6, 22).astype(np.float32)
base_b = (32 * (1 - dist*0.4)).clip(12, 42).astype(np.float32)

# Central vignette to ensure hero text always has high contrast
center_mask = (1.0 - 0.40 * np.exp(-((x - CX)**2 + (y - CY)**2) / (340**2))).astype(np.float32)

STATIC_BASE = np.stack([
    (base_r * center_mask).clip(0, 255).astype(np.uint8),
    (base_g * center_mask).clip(0, 255).astype(np.uint8),
    (base_b * center_mask).clip(0, 255).astype(np.uint8)
], axis=-1)

# Floating 3D particles
np.random.seed(42)
N_PARTICLES = 160
particle_coords = np.random.uniform([-950, -520, -350], [950, 520, 750], size=(N_PARTICLES, 3))
particle_alphas = np.random.uniform(50, 140, size=N_PARTICLES)
particle_radii = np.random.uniform(1.2, 2.6, size=N_PARTICLES)

def project_3d(x, y, z, yaw, pitch, roll=0, cam_dist=1100, fov=900):
    cy, sy = math.cos(yaw), math.sin(yaw)
    x1 = x * cy + z * sy
    y1 = y
    z1 = -x * sy + z * cy
    
    cp, sp = math.cos(pitch), math.sin(pitch)
    x2 = x1
    y2 = y1 * cp - z1 * sp
    z2 = y1 * sp + z1 * cp
    
    z_cam = z2 + cam_dist
    if z_cam <= 20:
        z_cam = 20
        
    scale = fov / z_cam
    sx = CX + x2 * scale
    sy = CY + y2 * scale
    return sx, sy, scale, z2

def get_base_canvas(t):
    img = Image.fromarray(STATIC_BASE.copy())
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Render ambient 3D particle dust
    for i in range(N_PARTICLES):
        px, py, pz = particle_coords[i]
        px_cur = px + math.sin(t * 0.4 + i) * 35
        py_cur = py + math.cos(t * 0.3 + i * 1.3) * 25
        pz_cur = pz + math.sin(t * 0.25 + i * 0.8) * 30
        
        sx, sy, scale, depth = project_3d(px_cur, py_cur, pz_cur, yaw=t*0.05, pitch=math.sin(t*0.04)*0.06)
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            rad = particle_radii[i] * scale * 1.2
            alpha = int(particle_alphas[i] * min(1.0, scale * 1.3))
            draw.ellipse([sx-rad, sy-rad, sx+rad, sy+rad], fill=(60, 190, 255, alpha))
            
    return img

# ==============================================================================
# SCENE 1: ARTIFICIAL INTELLIGENCE & NEURAL NETWORKS
# ==============================================================================
np.random.seed(101)
nn_layers_nodes = []
# Layer 0: Input (7 nodes)
nn_layers_nodes.append([(-520, y, np.random.uniform(-120, 120)) for y in np.linspace(-260, 260, 7)])
# Layer 1: Hidden 1 (12 nodes in 3D ellipsoid)
h1 = []
for i in range(12):
    ang = i * (2 * math.pi / 12)
    h1.append((-180, math.sin(ang)*280, math.cos(ang)*200))
nn_layers_nodes.append(h1)
# Layer 2: Hidden 2 (12 nodes in 3D ellipsoid)
h2 = []
for i in range(12):
    ang = i * (2 * math.pi / 12) + 0.26
    h2.append((180, math.sin(ang)*280, math.cos(ang)*200))
nn_layers_nodes.append(h2)
# Layer 3: Output (5 nodes)
nn_layers_nodes.append([(520, y, np.random.uniform(-120, 120)) for y in np.linspace(-220, 220, 5)])

def render_scene_1(t):
    img = get_base_canvas(t)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    yaw = 0.28 * math.sin(t * 0.5) + 0.12
    pitch = 0.12 * math.cos(t * 0.45) - 0.04
    
    proj_layers = []
    for layer in nn_layers_nodes:
        proj = [project_3d(pt[0], pt[1], pt[2], yaw, pitch) for pt in layer]
        proj_layers.append(proj)
        
    # Synaptic Connections
    for l_idx in range(len(proj_layers) - 1):
        l1 = proj_layers[l_idx]
        l2 = proj_layers[l_idx + 1]
        for i, (sx1, sy1, sc1, d1) in enumerate(l1):
            for j, (sx2, sy2, sc2, d2) in enumerate(l2):
                avg_depth = (d1 + d2) / 2
                depth_factor = np.clip(1.0 - (avg_depth / 800), 0.25, 1.25)
                pulse = (t * 2.8 + i * 0.35 + j * 0.2 + l_idx * 0.6) % 1.0
                alpha = int(40 * depth_factor)
                draw.line([(sx1, sy1), (sx2, sy2)], fill=(0, 140, 240, alpha), width=1)
                
                px = sx1 + (sx2 - sx1) * pulse
                py = sy1 + (sy2 - sy1) * pulse
                p_rad = 2.4 * depth_factor
                draw.ellipse([px-p_rad, py-p_rad, px+p_rad, py+p_rad], fill=(180, 245, 255, int(160 * depth_factor)))
                
    # Nodes with Radial Bloom
    for l_idx, layer in enumerate(proj_layers):
        for i, (sx, sy, scale, depth) in enumerate(layer):
            depth_factor = np.clip(1.0 - (depth / 700), 0.35, 1.35)
            activation = (math.sin(t * 3.8 + l_idx * 1.6 + i * 0.7) * 0.4 + 0.6) * depth_factor
            
            r_glow = 18 * scale * activation
            r_core = 6.5 * scale * activation
            draw.ellipse([sx-r_glow, sy-r_glow, sx+r_glow, sy+r_glow], fill=(0, 190, 255, int(50 * activation)))
            draw.ellipse([sx-r_core*1.6, sy-r_core*1.6, sx+r_core*1.6, sy+r_core*1.6], fill=(0, 220, 255, int(130 * activation)))
            draw.ellipse([sx-r_core, sy-r_core, sx+r_core, sy+r_core], fill=(225, 250, 255, 245))

    # Floating Technical HUD Metadata
    draw.text((90, 140), "NEURAL ARCHITECTURE // DEEP TENSOR LATTICE", font=font_code_bold, fill=(0, 225, 255, 230))
    draw.text((90, 172), "TENSOR SHAPE: [B, 512, 1024]  •  LOSS: 0.00114  •  ACCURACY: 99.46%", font=font_code_small, fill=(130, 190, 240, 190))
    draw.text((90, 198), "OPTIMIZER: ADAMW (LR=1e-4)  •  PARALLEL MULTI-GPU PIPELINE", font=font_code_small, fill=(0, 230, 255, 170))
    
    draw.text((WIDTH - 540, HEIGHT - 130), "TENSORFLOW // PYTORCH INFERENCE ENGINE", font=font_code_bold, fill=(0, 210, 255, 210))
    draw.text((WIDTH - 540, HEIGHT - 100), "REAL-TIME MATRIX MULTIPLICATION: 3.8 TFLOPS", font=font_code_small, fill=(110, 170, 230, 170))
    return img

# ==============================================================================
# SCENE 2: MODERN WEB DEVELOPMENT
# ==============================================================================
def render_scene_2(t):
    img = get_base_canvas(t)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    yaw = -0.26 + math.sin(t * 0.4) * 0.04
    pitch = 0.07 + math.cos(t * 0.35) * 0.03
    
    bw, bh = 1040, 580
    p_tl = project_3d(-bw/2, -bh/2, 0, yaw, pitch)
    p_tr = project_3d(bw/2, -bh/2, 0, yaw, pitch)
    p_br = project_3d(bw/2, bh/2, 0, yaw, pitch)
    p_bl = project_3d(-bw/2, bh/2, 0, yaw, pitch)
    
    # Outer 3D glow & shadow
    draw.polygon([(p_tl[0], p_tl[1]), (p_tr[0], p_tr[1]), (p_br[0], p_br[1]), (p_bl[0], p_bl[1])],
                 fill=(14, 20, 32, 235), outline=(0, 170, 255, 160))
                 
    # Browser Header Bar
    ph_bl = project_3d(-bw/2, -bh/2 + 50, 0, yaw, pitch)
    ph_br = project_3d(bw/2, -bh/2 + 50, 0, yaw, pitch)
    draw.polygon([(p_tl[0], p_tl[1]), (p_tr[0], p_tr[1]), (ph_br[0], ph_br[1]), (ph_bl[0], ph_bl[1])],
                 fill=(20, 28, 44, 255), outline=(0, 150, 230, 100))
                 
    # Window Dots (Red, Yellow, Green)
    for i, c_dot in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d_pt = project_3d(-bw/2 + 30 + i * 22, -bh/2 + 25, -5, yaw, pitch)
        draw.ellipse([d_pt[0]-5, d_pt[1]-5, d_pt[0]+5, d_pt[1]+5], fill=(c_dot[0], c_dot[1], c_dot[2], 230))
        
    # URL Pill Bar
    url_l = project_3d(-bw/2 + 110, -bh/2 + 15, -5, yaw, pitch)
    url_r = project_3d(bw/2 - 110, -bh/2 + 35, -5, yaw, pitch)
    draw.rounded_rectangle([url_l[0], url_l[1], url_r[0], url_r[1]], radius=8, fill=(10, 15, 24, 220), outline=(0, 140, 220, 80))
    url_t = project_3d(-bw/2 + 130, -bh/2 + 17, -8, yaw, pitch)
    draw.text((url_t[0], url_t[1]), "https://nithin-r.dev/dashboard/ai-vision", font=font_code_tiny, fill=(120, 190, 255, 210))
    
    # Left Pane: Code Editor (offset forward in 3D: z = -45)
    cw, ch = 470, 470
    pc_tl = project_3d(-bw/2 + 25, -bh/2 + 75, -45, yaw, pitch)
    pc_tr = project_3d(-bw/2 + 25 + cw, -bh/2 + 75, -45, yaw, pitch)
    pc_br = project_3d(-bw/2 + 25 + cw, -bh/2 + 75 + ch, -45, yaw, pitch)
    pc_bl = project_3d(-bw/2 + 25, -bh/2 + 75 + ch, -45, yaw, pitch)
    draw.polygon([(pc_tl[0], pc_tl[1]), (pc_tr[0], pc_tr[1]), (pc_br[0], pc_br[1]), (pc_bl[0], pc_bl[1])],
                 fill=(10, 14, 22, 245), outline=(0, 210, 255, 160))
                 
    code_texts = [
        ("import React, { useState } from 'react';", (180, 140, 255)),
        ("import { NeuralEngine } from '@lib/ai';", (0, 220, 255)),
        ("", (255, 255, 255)),
        ("const ModelClient = () => {", (255, 180, 60)),
        ("  const [liveData, setLiveData] = useState();", (120, 220, 255)),
        ("  useEffect(() => {", (255, 120, 180)),
        ("    engine.subscribe(data => {", (220, 230, 245)),
        ("      setLiveData(data.stream());", (140, 255, 160)),
        ("    });", (220, 230, 245)),
        ("  }, []);", (255, 120, 180)),
        ("  return <ReactiveGrid data={liveData} />;", (0, 230, 255)),
        ("};", (255, 180, 60)),
    ]
    for idx, (txt, col) in enumerate(code_texts):
        if not txt: continue
        pt = project_3d(-bw/2 + 45, -bh/2 + 105 + idx * 34, -45, yaw, pitch)
        draw.text((pt[0], pt[1]), txt, font=font_code_small, fill=(col[0], col[1], col[2], 230))
        
    # Right Pane: Interactive Web UI (offset forward in 3D: z = -65)
    rw, rh = 470, 470
    pui_tl = project_3d(bw/2 - 25 - rw, -bh/2 + 75, -65, yaw, pitch)
    pui_tr = project_3d(bw/2 - 25, -bh/2 + 75, -65, yaw, pitch)
    pui_br = project_3d(bw/2 - 25, -bh/2 + 75 + rh, -65, yaw, pitch)
    pui_bl = project_3d(bw/2 - 25 - rw, -bh/2 + 75 + rh, -65, yaw, pitch)
    draw.polygon([(pui_tl[0], pui_tl[1]), (pui_tr[0], pui_tr[1]), (pui_br[0], pui_br[1]), (pui_bl[0], pui_bl[1])],
                 fill=(16, 24, 38, 245), outline=(0, 190, 255, 170))
                 
    # Card 1 inside UI
    c1_tl = project_3d(bw/2 - 25 - rw + 20, -bh/2 + 95, -75, yaw, pitch)
    c1_br = project_3d(bw/2 - 45, -bh/2 + 185, -75, yaw, pitch)
    draw.rounded_rectangle([c1_tl[0], c1_tl[1], c1_br[0], c1_br[1]], radius=8, fill=(22, 32, 52, 230), outline=(0, 180, 255, 120))
    t1 = project_3d(bw/2 - 25 - rw + 35, -bh/2 + 110, -78, yaw, pitch)
    draw.text((t1[0], t1[1]), "Real-Time AI Inference", font=font_ui_bold, fill=(240, 250, 255, 255))
    t2 = project_3d(bw/2 - 25 - rw + 35, -bh/2 + 145, -78, yaw, pitch)
    draw.text((t2[0], t2[1]), "Accuracy: 99.8%  •  Latency: 4.2ms", font=font_code_tiny, fill=(0, 220, 255, 220))
    
    # Animated Graph Widget inside UI
    graph_pts = []
    for step in range(11):
        gx = bw/2 - 25 - rw + 35 + step * (rw - 70) / 10
        gy = -bh/2 + 330 - math.sin(step * 0.65 + t * 4) * 45
        graph_pts.append(project_3d(gx, gy, -80, yaw, pitch)[:2])
    draw.line(graph_pts, fill=(0, 240, 255, 240), width=2)
    for gpt in graph_pts:
        draw.ellipse([gpt[0]-3.5, gpt[1]-3.5, gpt[0]+3.5, gpt[1]+3.5], fill=(220, 255, 255, 255))
        
    draw.text((90, 140), "MODERN WEB INFRASTRUCTURE // REACT • TYPESCRIPT • CSS GRID", font=font_code_bold, fill=(0, 220, 255, 220))
    draw.text((90, 172), "FULL-STACK CLIENT ARCHITECTURE • WEBSOCKET REAL-TIME STREAMING", font=font_code_small, fill=(120, 180, 230, 180))
    return img

# ==============================================================================
# SCENE 3: MOBILE APP DEVELOPMENT
# ==============================================================================
def render_scene_3(t):
    img = get_base_canvas(t)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    phone_offset_x = 280
    yaw = 0.32 + math.sin(t * 0.4) * 0.05
    pitch = -0.10 + math.cos(t * 0.35) * 0.04
    
    pw, ph = 350, 700
    p_tl = project_3d(phone_offset_x - pw/2, -ph/2, 0, yaw, pitch)
    p_tr = project_3d(phone_offset_x + pw/2, -ph/2, 0, yaw, pitch)
    p_br = project_3d(phone_offset_x + pw/2, ph/2, 0, yaw, pitch)
    p_bl = project_3d(phone_offset_x - pw/2, ph/2, 0, yaw, pitch)
    
    # Outer Bezel
    draw.polygon([(p_tl[0], p_tl[1]), (p_tr[0], p_tr[1]), (p_br[0], p_br[1]), (p_bl[0], p_bl[1])],
                 fill=(26, 32, 46, 255), outline=(0, 190, 255, 220))
                 
    # Screen Quad
    sw, sh = pw - 24, ph - 28
    s_tl = project_3d(phone_offset_x - sw/2, -sh/2, -8, yaw, pitch)
    s_tr = project_3d(phone_offset_x + sw/2, -sh/2, -8, yaw, pitch)
    s_br = project_3d(phone_offset_x + sw/2, sh/2, -8, yaw, pitch)
    s_bl = project_3d(phone_offset_x - sw/2, sh/2, -8, yaw, pitch)
    draw.polygon([(s_tl[0], s_tl[1]), (s_tr[0], s_tr[1]), (s_br[0], s_br[1]), (s_bl[0], s_bl[1])],
                 fill=(10, 14, 22, 255), outline=(0, 150, 230, 140))
                 
    # Dynamic Island / Camera Notch
    notch_l = project_3d(phone_offset_x - 50, -sh/2 + 15, -12, yaw, pitch)
    notch_r = project_3d(phone_offset_x + 50, -sh/2 + 35, -12, yaw, pitch)
    draw.rounded_rectangle([notch_l[0], notch_l[1], notch_r[0], notch_r[1]], radius=9, fill=(0, 0, 0, 255), outline=(40, 60, 90, 180))
    
    # App Header inside Screen
    th_1 = project_3d(phone_offset_x - sw/2 + 25, -sh/2 + 55, -14, yaw, pitch)
    draw.text((th_1[0], th_1[1]), "AI Vision Scanner", font=font_ui_bold, fill=(240, 250, 255, 255))
    th_2 = project_3d(phone_offset_x - sw/2 + 25, -sh/2 + 88, -14, yaw, pitch)
    draw.text((th_2[0], th_2[1]), "COREML // TFLITE ACCELERATION", font=font_code_tiny, fill=(0, 220, 255, 210))
    
    # 3D Floating Holographic Vision Card (hovering 65px forward in 3D: z = -75)
    cw, ch = 280, 290
    card_y = -30
    c_tl_f = project_3d(phone_offset_x - cw/2, card_y - ch/2, -75, yaw, pitch)
    c_tr_f = project_3d(phone_offset_x + cw/2, card_y - ch/2, -75, yaw, pitch)
    c_br_f = project_3d(phone_offset_x + cw/2, card_y + ch/2, -75, yaw, pitch)
    c_bl_f = project_3d(phone_offset_x - cw/2, card_y + ch/2, -75, yaw, pitch)
    draw.polygon([(c_tl_f[0], c_tl_f[1]), (c_tr_f[0], c_tr_f[1]), (c_br_f[0], c_br_f[1]), (c_bl_f[0], c_bl_f[1])],
                 fill=(16, 24, 38, 245), outline=(0, 230, 255, 200))
                 
    # Scanner Reticle & Laser Sweep
    scan_t = (t * 1.6) % 1.0
    scan_y_local = card_y - ch/2 + 35 + scan_t * (ch - 70)
    sl_1 = project_3d(phone_offset_x - cw/2 + 20, scan_y_local, -80, yaw, pitch)
    sl_2 = project_3d(phone_offset_x + cw/2 - 20, scan_y_local, -80, yaw, pitch)
    draw.line([(sl_1[0], sl_1[1]), (sl_2[0], sl_2[1])], fill=(0, 245, 255, 230), width=2)
    
    # Corner Reticle Markers
    for ox, oy in [(-cw/2+20, card_y-ch/2+20), (cw/2-35, card_y-ch/2+20), (-cw/2+20, card_y+ch/2-35), (cw/2-35, card_y+ch/2-35)]:
        p1 = project_3d(phone_offset_x + ox, oy, -80, yaw, pitch)
        p2 = project_3d(phone_offset_x + ox + 15, oy + 15, -80, yaw, pitch)
        draw.rectangle([p1[0], p1[1], p2[0], p2[1]], outline=(0, 240, 255, 220), width=2)
        
    t_pos = project_3d(phone_offset_x - cw/2 + 25, card_y + ch/2 - 55, -80, yaw, pitch)
    draw.text((t_pos[0], t_pos[1]), "CLASSIFICATION: DETECTED (99.2%)", font=font_code_tiny, fill=(0, 240, 255, 230))
    t_pos2 = project_3d(phone_offset_x - cw/2 + 25, card_y + ch/2 - 30, -80, yaw, pitch)
    draw.text((t_pos2[0], t_pos2[1]), "LATENCY: 8ms (NEURAL ENGINE)", font=font_code_tiny, fill=(150, 210, 255, 190))
    
    # Bottom Tab Navigation on Phone
    b_nav_1 = project_3d(phone_offset_x - sw/2 + 15, sh/2 - 60, -12, yaw, pitch)
    b_nav_2 = project_3d(phone_offset_x + sw/2 - 15, sh/2 - 15, -12, yaw, pitch)
    draw.rounded_rectangle([b_nav_1[0], b_nav_1[1], b_nav_2[0], b_nav_2[1]], radius=12, fill=(18, 26, 42, 230), outline=(30, 60, 90, 140))
    nav_pos = project_3d(phone_offset_x - sw/2 + 35, sh/2 - 45, -15, yaw, pitch)
    draw.text((nav_pos[0], nav_pos[1]), "Home    Scanner    Analytics    Settings", font=font_code_tiny, fill=(100, 170, 230, 200))
    
    # Left Side Specifications
    draw.text((90, HEIGHT * 0.32), "MOBILE APPLICATION ENGINEERING", font=font_code_bold, fill=(0, 220, 255, 220))
    draw.text((90, HEIGHT * 0.37), "• Cross-Platform iOS & Android Systems", font=font_code, fill=(210, 235, 255, 220))
    draw.text((90, HEIGHT * 0.42), "• Hardware-Accelerated ML (TFLite / CoreML)", font=font_code, fill=(210, 235, 255, 220))
    draw.text((90, HEIGHT * 0.47), "• 60 FPS Native Touch Gesture Engine", font=font_code, fill=(210, 235, 255, 220))
    draw.text((90, HEIGHT * 0.52), "• Offline-First Distributed Synchronization", font=font_code, fill=(210, 235, 255, 220))
    return img

# ==============================================================================
# SCENE 4: SOFTWARE ENGINEERING & DISTRIBUTED CLOUD
# ==============================================================================
def render_scene_4(t):
    img = get_base_canvas(t)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    tx, ty, tw, th = 80, 220, 800, 560
    draw.rounded_rectangle([tx, ty, tx+tw, ty+th], radius=14, fill=(10, 14, 22, 240), outline=(0, 170, 255, 140))
    draw.rectangle([tx, ty, tx+tw, ty+40], fill=(18, 26, 40, 255))
    draw.text((tx+20, ty+10), "server_pipeline.py  (Python 3.12 / Flask / Torch)", font=font_code_small, fill=(0, 225, 255, 220))
    
    py_code = [
        ("@app.route('/v1/predict', methods=['POST'])", (255, 200, 60)),
        ("def dispatch_inference_request():", (120, 220, 255)),
        ("    payload = request.get_json()", (220, 235, 250)),
        ("    # Check Redis Cache for Precomputed Tensors", (100, 150, 200)),
        ("    cache_key = hashlib.sha256(payload).hexdigest()", (140, 255, 160)),
        ("    if cached := redis_cluster.get(cache_key):", (255, 120, 180)),
        ("        return jsonify({'cached': True, 'result': cached})", (140, 255, 160)),
        ("    # Distributed PyTorch GPU Compute", (100, 150, 200)),
        ("    tensor_batch = torch.tensor(payload['data']).cuda()", (220, 235, 250)),
        ("    predictions = model_ensemble(tensor_batch)", (0, 240, 255)),
        ("    db_session.log_telemetry(predictions.metrics)", (180, 140, 255)),
        ("    return jsonify({'status': 'SUCCESS', 'data': predictions})", (140, 255, 160)),
    ]
    for idx, (code, col) in enumerate(py_code):
        draw.text((tx+20, ty+54+idx*36), f"{idx+1:2d}  {code}", font=font_code, fill=(col[0], col[1], col[2], 230))
        
    arch_cx = WIDTH - 480
    arch_cy = HEIGHT / 2 + 30
    nodes = [
        (arch_cx, arch_cy - 200, "CLIENT / MOBILE", (0, 200, 255)),
        (arch_cx, arch_cy - 90, "API GATEWAY & LOAD BALANCER", (40, 225, 205)),
        (arch_cx - 160, arch_cy + 40, "AI INFERENCE ENGINE", (180, 140, 255)),
        (arch_cx + 160, arch_cy + 40, "MICROSERVICES CLUSTER", (255, 180, 70)),
        (arch_cx, arch_cy + 170, "POSTGRESQL & REDIS CLUSTER", (80, 225, 145)),
    ]
    for i1, i2 in [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)]:
        x1, y1, _, _ = nodes[i1]
        x2, y2, _, _ = nodes[i2]
        draw.line([(x1, y1), (x2, y2)], fill=(0, 140, 220, 140), width=2)
        p = (t * 2.4 + i1 * 0.4) % 1.0
        px = x1 + (x2 - x1) * p
        py = y1 + (y2 - y1) * p
        draw.ellipse([px-4.5, py-4.5, px+4.5, py+4.5], fill=(225, 255, 255, 255))
        
    for nx, ny, label, col in nodes:
        draw.rounded_rectangle([nx-140, ny-24, nx+140, ny+24], radius=10, fill=(16, 24, 38, 255), outline=col, width=2)
        draw.text((nx-120, ny-12), label, font=font_code_small, fill=(col[0], col[1], col[2], 245))
        
    draw.text((WIDTH - 700, 140), "SOFTWARE ENGINEERING & DISTRIBUTED SYSTEMS", font=font_code_bold, fill=(0, 220, 255, 220))
    return img

# ==============================================================================
# SCENE 5: UNIFIED TECHNOLOGY CONVERGENCE (THE DIGITAL NEXUS)
# ==============================================================================
def render_scene_5(t):
    img = get_base_canvas(t)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    yaw = t * 0.35
    pitch = 0.16 * math.sin(t * 0.3)
    
    r_orbit = 540
    pillars = [
        ("AI & MACHINE LEARNING", "Neural Networks • PyTorch • Deep Learning", 0, (0, 230, 255)),
        ("WEB DEVELOPMENT", "Full-Stack • React • Responsive UI", math.pi/2, (0, 190, 255)),
        ("MOBILE DEVELOPMENT", "Cross-Platform • Native Systems", math.pi, (120, 210, 255)),
        ("SOFTWARE ENGINEERING", "Distributed Systems • Python Core", 3*math.pi/2, (160, 200, 255)),
    ]
    
    # 3D Rotating Central Geodesic Ring Sphere
    core_rad = 54 + math.sin(t * 3.5) * 6
    for halo_r, alpha in [(core_rad * 2.8, 20), (core_rad * 1.9, 50), (core_rad * 1.3, 110)]:
        draw.ellipse([CX-halo_r, CY-halo_r, CX+halo_r, CY+halo_r], fill=(0, 160, 255, alpha))
        
    # Orbiting Rings in 3D
    ring_pts = []
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        rx = math.cos(rad) * 110
        ry = math.sin(rad) * 110
        rz = math.sin(rad + t*2) * 60
        sx, sy, sc, dp = project_3d(rx, ry, rz, yaw=t*0.5, pitch=0.4)
        ring_pts.append((sx, sy))
    if ring_pts:
        draw.line(ring_pts + [ring_pts[0]], fill=(0, 220, 255, 140), width=2)
        
    draw.ellipse([CX-core_rad, CY-core_rad, CX+core_rad, CY+core_rad], fill=(210, 245, 255, 245), outline=(0, 230, 255, 255), width=2)
    
    for title, subtitle, base_ang, col in pillars:
        ang = base_ang + yaw
        px = math.cos(ang) * r_orbit
        pz = math.sin(ang) * (r_orbit * 0.7)
        py = math.sin(ang * 2) * 60
        
        sx, sy, scale, depth = project_3d(px, py, pz, yaw=0, pitch=pitch)
        depth_factor = np.clip(1.0 - (depth / 800), 0.4, 1.3)
        
        draw.line([(CX, CY), (sx, sy)], fill=(0, 160, 240, int(120 * depth_factor)), width=2)
        pulse = (t * 2.2 + base_ang) % 1.0
        pulse_x = CX + (sx - CX) * pulse
        pulse_y = CY + (sy - CY) * pulse
        draw.ellipse([pulse_x-4.5, pulse_y-4.5, pulse_x+4.5, pulse_y+4.5], fill=(225, 255, 255, 255))
        
        bw = 320 * scale
        bh = 76 * scale
        draw.rounded_rectangle([sx-bw/2, sy-bh/2, sx+bw/2, sy+bh/2], radius=12, fill=(14, 20, 34, int(235 * depth_factor)), outline=col, width=2)
        draw.text((sx-bw/2 + 20, sy-bh/2 + 14), title, font=font_code_bold, fill=(col[0], col[1], col[2], int(245 * depth_factor)))
        draw.text((sx-bw/2 + 20, sy-bh/2 + 42), subtitle, font=font_code_small, fill=(160, 205, 245, int(190 * depth_factor)))
        
    return img
