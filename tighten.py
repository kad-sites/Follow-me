import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make vertical padding/margins much tighter
html = re.sub(r'(\.section\s*\{[^}]*)padding:\s*16px;', r'\1padding: 10px 16px;', html)
html = re.sub(r'(\.section\s*\{[^}]*)margin-bottom:\s*12px;', r'\1margin-bottom: 8px;', html)

html = re.sub(r'(\.section-header\s*\{[^}]*)margin-bottom:\s*8px;', r'\1margin-bottom: 4px;', html)

html = re.sub(r'(\.panel-header\s*\{[^}]*)padding:\s*16px\s*20px;', r'\1padding: 10px 16px;', html)

html = re.sub(r'(\.tv-effect-btn\s*\{[^}]*)padding:\s*10px\s*14px;', r'\1padding: 8px 14px;', html)
html = re.sub(r'(\.tv-effect-btn\s*\{[^}]*)margin-bottom:\s*8px;', r'\1margin-bottom: 4px;', html)

html = html.replace('margin: 16px 0;', 'margin: 8px 0;')

# Re-enlarge fonts and swatches to maintain horizontal/usability sizing
html = re.sub(r'(\.tv-effect-btn\s*\{[^}]*)font-size:\s*13px;', r'\1font-size: 14px;', html)
html = re.sub(r'(\.color-swatch\s*\{[^}]*)width:\s*28px;', r'\1width: 32px;', html)
html = re.sub(r'(\.color-swatch\s*\{[^}]*)height:\s*28px;', r'\1height: 32px;', html)
html = re.sub(r'(input\[type="range"\]::-webkit-slider-thumb\s*\{[^}]*)width:\s*20px;', r'\1width: 24px;', html)
html = re.sub(r'(input\[type="range"\]::-webkit-slider-thumb\s*\{[^}]*)height:\s*20px;', r'\1height: 24px;', html)
html = re.sub(r'(input\[type="range"\]::-webkit-slider-thumb\s*\{[^}]*)margin-top:\s*-7px;', r'\1margin-top: -9px;', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
