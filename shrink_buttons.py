import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make color-swatch smaller
html = re.sub(r'(\.color-swatch\s*\{[^}]*)width:\s*32px;', r'\1width: 26px;', html)
html = re.sub(r'(\.color-swatch\s*\{[^}]*)height:\s*32px;', r'\1height: 26px;', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
