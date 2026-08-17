import sys, re
with open('index.html', 'r') as f:
    html = f.read()

html = re.sub(r'\s*<div class="section-header">\s*<div class="section-title">Active Pixels</div>\s*<div class="value-display" id="pixelsVal">180</div>\s*</div>\s*<div class="slider-container">\s*<input type="range" id="activePixels" min="10" max="300" value="180">\s*</div>\s*<div style="display: flex; justify-content: space-between; font-size: 10px; color: var\(--subtext\); margin-bottom: 24px;">\s*<span>10</span><span>300</span>\s*</div>', '', html)

with open('index.html', 'w') as f:
    f.write(html)
