import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make section padding smaller
html = re.sub(r'(\.section\s*\{[^}]*)padding:\s*20px;', r'\1padding: 16px;', html)
html = re.sub(r'(\.section\s*\{[^}]*)border-radius:\s*16px;', r'\1border-radius: 12px;', html)
html = re.sub(r'(\.section\s*\{)', r'\1\n            margin-bottom: 12px;', html)

# Make section header margin smaller
html = re.sub(r'(\.section-header\s*\{[^}]*)margin-bottom:\s*12px;', r'\1margin-bottom: 8px;', html)

# Sliders
html = re.sub(r'(input\[type="range"\]\s*\{[^}]*)height:\s*8px;', r'\1height: 6px;', html)
html = re.sub(r'(input\[type="range"\]::-webkit-slider-thumb\s*\{[^}]*)width:\s*24px;', r'\1width: 20px;', html)
html = re.sub(r'(input\[type="range"\]::-webkit-slider-thumb\s*\{[^}]*)height:\s*24px;', r'\1height: 20px;', html)
html = re.sub(r'(input\[type="range"\]::-webkit-slider-thumb\s*\{[^}]*)margin-top:\s*-8px;', r'\1margin-top: -7px;', html)

# Buttons
html = re.sub(r'(\.tv-effect-btn\s*\{[^}]*)padding:\s*12px\s*16px;', r'\1padding: 10px 14px;', html)
html = re.sub(r'(\.tv-effect-btn\s*\{[^}]*)font-size:\s*14px;', r'\1font-size: 13px;', html)

# Color swatches
html = re.sub(r'(\.color-swatch\s*\{[^}]*)width:\s*32px;', r'\1width: 28px;', html)
html = re.sub(r'(\.color-swatch\s*\{[^}]*)height:\s*32px;', r'\1height: 28px;', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
