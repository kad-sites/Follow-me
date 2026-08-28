with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Change the TV brightness slider default in the HTML from 255 to 30
html = re.sub(r'id="tvBrightness" min="0" max="255" value="255"', 'id="tvBrightness" min="0" max="255" value="30"', html)
html = re.sub(r'<div class="value-display" id="tvBrightVal">100%</div>', '<div class="value-display" id="tvBrightVal">12%</div>', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
