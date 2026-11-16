import urllib.request
import os

base_dir = r"C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio"

routes = [
    ('/', 'index.html'),
    ('/contact', 'contact.html'),
    ('/cv', 'bio.html'),
]

for route, filename in routes:
    url = f"http://127.0.0.1:5000{route}"
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        # Convert absolute /static/ to relative ./static/
        html = html.replace('href="/static/', 'href="./static/')
        html = html.replace('src="/static/', 'src="./static/')
        # Convert links
        html = html.replace('href="/home"', 'href="./index.html"')
        html = html.replace('href="/"', 'href="./index.html"')
        html = html.replace('href="/contact"', 'href="./contact.html"')
        html = html.replace('href="/cv"', 'href="./bio.html"')
        
        target_path = os.path.join(base_dir, filename)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Successfully generated {target_path} ({len(html)} bytes)")
    except Exception as e:
        print(f"Error exporting {route}: {e}")
