import os
import sys
import math
import time
import shutil
import subprocess
import numpy as np
from PIL import Image
import imageio_ffmpeg

import render_engine as re

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
base_dir = r"C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio"
output_video = os.path.join(base_dir, "static", "images", "hero_video.mp4")
backup_video = os.path.join(base_dir, "static", "images", "hero_video_original.mp4")

# Backup original video if not already backed up
if os.path.exists(output_video) and not os.path.exists(backup_video):
    shutil.copy2(output_video, backup_video)
    print(f"Backed up original video to {backup_video}")

WIDTH, HEIGHT = 1920, 1080
FPS = 30
DURATION = 15.0 # seconds
TOTAL_FRAMES = int(FPS * DURATION) # 450 frames
SCENE_DURATION = 3.0 # seconds per scene
TRANSITION_DUR = 0.7 # seconds of crossfade

scene_funcs = [
    re.render_scene_1, # Scene 1: AI / Neural Networks
    re.render_scene_2, # Scene 2: Web Development
    re.render_scene_3, # Scene 3: Mobile App Development
    re.render_scene_4, # Scene 4: Software Engineering & Cloud
    re.render_scene_5, # Scene 5: Unified Nexus
]

def get_frame(f_idx):
    t = f_idx / FPS
    # Determine current scene index (0 to 4)
    scene_idx = int(t / SCENE_DURATION) % 5
    t_in_scene = t - (scene_idx * SCENE_DURATION)
    
    # Check if we are in crossfade window near end of scene
    if t_in_scene >= (SCENE_DURATION - TRANSITION_DUR):
        next_scene_idx = (scene_idx + 1) % 5
        progress = (t_in_scene - (SCENE_DURATION - TRANSITION_DUR)) / TRANSITION_DUR
        # Smooth cosine interpolation
        smooth_alpha = 0.5 - 0.5 * math.cos(progress * math.pi)
        
        # Render scene A
        img_a = np.array(scene_funcs[scene_idx](t), dtype=np.float32)
        # Render scene B (for seamless loop, if next is 0, t starts at 0.0)
        t_b = t if next_scene_idx != 0 else (t - DURATION)
        img_b = np.array(scene_funcs[next_scene_idx](t_b), dtype=np.float32)
        
        blended = (1.0 - smooth_alpha) * img_a + smooth_alpha * img_b
        return blended.clip(0, 255).astype(np.uint8)
    else:
        # Pure scene
        return np.array(scene_funcs[scene_idx](t), dtype=np.uint8)

print(f"Starting cinematic video generation: {TOTAL_FRAMES} frames @ {FPS} fps...")
t_start = time.time()

# Launch ffmpeg process with stdin pipe
ffmpeg_cmd = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    output_video
]

process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

for f in range(TOTAL_FRAMES):
    frame = get_frame(f)
    process.stdin.write(frame.tobytes())
    if f % 45 == 0 or f == TOTAL_FRAMES - 1:
        pct = (f + 1) / TOTAL_FRAMES * 100
        print(f"Progress: frame {f+1}/{TOTAL_FRAMES} ({pct:.1f}%)")

process.stdin.close()
out, err = process.communicate()
rc = process.returncode

t_end = time.time()
if rc == 0 and os.path.exists(output_video):
    size_mb = os.path.getsize(output_video) / (1024 * 1024)
    print(f"\nSUCCESS! Generated {output_video} in {t_end - t_start:.1f}s")
    print(f"Video size: {size_mb:.2f} MB, Resolution: {WIDTH}x{HEIGHT}, FPS: {FPS}, Duration: {DURATION}s")
else:
    print(f"Error generating video (code {rc}):")
    print(err.decode('utf-8', errors='ignore'))
