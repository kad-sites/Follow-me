import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'\s*<button class="apply-btn" id="applyRadarBtn" onclick="applyRadarSettings\(\)">Apply to Sensor</button>', '', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
