import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace Pixora checkbox switch with sleek power button
power_regex = r'<label class="switch">\s*<input type="checkbox" id="pxPower"[^>]*>\s*<span class="slider round"></span>\s*</label>'
new_power = '<button id="pxPowerBtn" onclick="togglePxPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; height: 32px; padding: 0 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s; box-sizing: border-box;">ON</button>'
html = re.sub(power_regex, new_power, html)

# Add style="margin-top:0;" to px-effect-btn just in case
html = html.replace('class="tv-effect-btn px-effect-btn"', 'class="tv-effect-btn px-effect-btn" style="margin-top:0;"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
