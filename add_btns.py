# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

target = """<button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, 
'fire')">2D Fire</button>""".replace("\n", "")

# The actual file has a newline in it in my grep output! Let's do it cleanly:
import re
new_html = re.sub(r'(<button[^>]+onclick="setPxEffect\(this,\s*\'fire\'\)">2D Fire</button>)',
                  r'\1\n                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, \'fireworks\')\">Fireworks</button>\n                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, \'vu_meter\')\">VU Meter</button>',
                  html)

if new_html != html:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Buttons added!")
else:
    print("Regex failed")
