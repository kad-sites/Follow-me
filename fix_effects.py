with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
old_btn = r'<button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect\(this, \'rainbow\'\)">Rainbow Flow</button>'
new_btns = """<button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'rainbow')">Rainbow Flow</button>
                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'chase')">Theater Chase</button>
                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'twinkle')">Starry Twinkle</button>
                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'fire')">Fire Effect</button>"""
html = re.sub(old_btn, new_btns, html)

# Also fix the power button text toggle in main.js since I changed it to say "ON" and "OFF" (slimmer)
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace('btn.innerText = "TURN OFF";', 'btn.innerText = "ON";')
js = js.replace('btn.innerText = "TURN ON";', 'btn.innerText = "OFF";')
with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
