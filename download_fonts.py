import os
import json
import re
import urllib.request

js_path = r'C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio\static\js\typekit_source.js'
fonts_dir = r'C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio\static\fonts'
os.makedirs(fonts_dir, exist_ok=True)

with open(js_path, encoding='utf-8') as f:
    s = f.read()

m = re.search(r'window\.Typekit\.config\s*=\s*(\{.+?\});', s)
conf = json.loads(m.group(1))

css_rules = []
for i, item in enumerate(conf['fc']):
    fam = item['family']
    desc = item['descriptors']
    weight = desc['weight']
    style = desc['style']
    src_tmpl = item['src']
    url = src_tmpl.split('{format}')[0] + 'a'
    fname = f"{fam}_{weight}_{style}.otf"
    fpath = os.path.join(fonts_dir, fname)
    if not os.path.exists(fpath):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
            with open(fpath, 'wb') as out:
                out.write(data)
            print(f"Downloaded {fname}: {len(data)} bytes")
        except Exception as e:
            print(f"Failed {fname}: {e}")
    else:
        print(f"Already have {fname}")

    real_name = "Adrianna Extended" if fam == "cxxc" else ("Acumin Pro Wide" if fam == "vcxq" else fam)
    rule = f"""@font-face {{
  font-family: '{fam}';
  font-style: {style};
  font-weight: {weight};
  src: url('/static/fonts/{fname}') format('opentype');
  font-display: swap;
}}
@font-face {{
  font-family: '{real_name}';
  font-style: {style};
  font-weight: {weight};
  src: url('/static/fonts/{fname}') format('opentype');
  font-display: swap;
}}
"""
    css_rules.append(rule)

css_path = os.path.join(fonts_dir, 'fonts.css')
with open(css_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(css_rules))

print("Successfully wrote fonts.css!")
