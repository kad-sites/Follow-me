with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# 1. Replace the checkbox toggle with the TV-style button
old_px_power = """                    <label class="switch">
                        <input type="checkbox" id="pxPower" onchange="togglePxPower()" checked>
                        <span class="slider round"></span>
                    </label>"""
new_px_power = """                    <button id="pxPowerBtn" onclick="togglePxPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; height: 32px; padding: 0 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s; box-sizing: border-box;">ON</button>"""
html = html.replace(old_px_power, new_px_power)

# 2. Change effect-btn to tv-effect-btn for the Pixora effect dropdown
html = html.replace('class="effect-btn px-effect-btn', 'class="tv-effect-btn px-effect-btn')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
