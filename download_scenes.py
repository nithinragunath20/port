import urllib.request
import os
import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
work_dir = r"C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio\video_work"
os.makedirs(work_dir, exist_ok=True)

clips = [
    ("scene1_ai", "https://assets.mixkit.co/videos/4908/4908-720.mp4"),
    ("scene1_ai_30869", "https://assets.mixkit.co/videos/30869/30869-720.mp4"),
    ("scene2_web", "https://assets.mixkit.co/videos/4192/4192-720.mp4"),
    ("scene3_mobile", "https://assets.mixkit.co/videos/42136/42136-720.mp4"),
    ("scene4_code", "https://assets.mixkit.co/videos/41658/41658-720.mp4"),
    ("scene5_unified", "https://assets.mixkit.co/videos/31542/31542-720.mp4"),
]

for name, url in clips:
    mp4_path = os.path.join(work_dir, f"{name}.mp4")
    png_path = os.path.join(work_dir, f"{name}.jpg")
    print(f"Downloading {name}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r, open(mp4_path, 'wb') as f:
        f.write(r.read())
    print(f"Downloaded {name} ({os.path.getsize(mp4_path)} bytes)")
    # Extract frame at 2.0s
    subprocess.run([ffmpeg_exe, "-y", "-ss", "00:00:02", "-i", mp4_path, "-vframes", "1", png_path],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Extracted preview for {name}")

print("All clips downloaded.")
