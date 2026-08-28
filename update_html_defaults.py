import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update initial display values and slider values
html = re.sub(r'<div class="value-display" id="fBrightVal">\d+%</div>', '<div class="value-display" id="fBrightVal">50%</div>', html)
html = re.sub(r'id="followBrightness" min="0" max="255" value="\d+"', 'id="followBrightness" min="0" max="255" value="127"', html)

html = re.sub(r'<div class="value-display" id="bBrightVal">\d+%</div>', '<div class="value-display" id="bBrightVal">0%</div>', html)
html = re.sub(r'id="baseBrightness" min="0" max="255" value="\d+"', 'id="baseBrightness" min="0" max="255" value="0"', html)

html = re.sub(r'<div class="value-display" id="leadVal">\d+</div>', '<div class="value-display" id="leadVal">6</div>', html)
html = re.sub(r'id="leadFactor" min="0" max="50" value="\d+"', 'id="leadFactor" min="0" max="50" value="6"', html)

html = re.sub(r'<div class="value-display" id="glowVal">\d+</div>', '<div class="value-display" id="glowVal">10</div>', html)
html = re.sub(r'id="glowSize" min="6" max="60" value="\d+"', 'id="glowSize" min="6" max="60" value="10"', html)

html = re.sub(r'<div class="value-display" id="activeVal">\d+</div>', '<div class="value-display" id="activeVal">150</div>', html)
html = re.sub(r'id="activePixels" min="10" max="300" value="\d+"', 'id="activePixels" min="10" max="300" value="150"', html)

html = re.sub(r'<div class="value-display" id="fadeVal">\d+</div>', '<div class="value-display" id="fadeVal">0</div>', html)
html = re.sub(r'id="fadeSigma" min="10" max="100" value="\d+"', 'id="fadeSigma" min="0" max="100" value="0"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
