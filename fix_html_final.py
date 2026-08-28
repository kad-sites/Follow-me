import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<div id="radarArrow" style="color: var\(--subtext\); font-size: 12px;">.*?</div>', '<div id="radarArrow" style="color: var(--subtext); font-size: 12px;">&#9660;</div>', html)
html = re.sub(r'Advanced <span id="advArrow">.*?</span>', 'Advanced <span id="advArrow">&#9660;</span>', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
