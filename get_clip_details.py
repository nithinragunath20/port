import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

video_ids = [1728, 50748, 242, 4908, 4872, 46635, 31590, 31542, 32989, 47321, 48579, 46036, 45677, 46038, 41642]

details = {}
for vid in video_ids:
    url = f"https://mixkit.co/free-stock-video/item/{vid}/"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        title_match = re.search(r'<title>(.*?)</title>', html)
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html)
        title = h1_match.group(1).strip() if h1_match else (title_match.group(1).strip() if title_match else f"Video {vid}")
        # Look for 1080p download URL
        f1080 = f"https://assets.mixkit.co/videos/{vid}/{vid}-1080.mp4"
        details[vid] = {"title": title, "url": f1080}
        print(f"ID {vid}: {title}")
    except Exception as e:
        print(f"Error {vid}: {e}")

with open(r"C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio\clip_details.json", "w") as f:
    json.dump(details, f, indent=2)
