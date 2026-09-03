# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

target = 'onclick="setPxEffect(this, \\\'vu_meter\\\')\\">VU Meter</button>'

# Oh wait, the previous python script wrote `\'vu_meter\'\">` literally into the HTML file? Let me check that.
# Let's just find "VU Meter"
import re
new_html = re.sub(r'(>VU Meter</button>)',
                  r'\1\n                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, \'pacman\')">Pac-Man Chase</button>\n                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, \'falling_sand\')">Falling Sand</button>\n                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, \'smart_snake\')">Smart Snake</button>\n                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, \'warp_speed\')">Warp Speed</button>\n                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, \'rain_ripples\')">Rain Ripples</button>',
                  html)

if new_html != html:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Buttons added!")
else:
    print("Failed")
