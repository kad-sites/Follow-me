# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

target_btn = """<button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, 'tetris')">Tetris Animation</button>"""
new_btn = """<button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, 'tetris')">Tetris Animation</button>
                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, 'candy_crush')">Candy Crush</button>"""

if target_btn in html:
    html = html.replace(target_btn, new_btn)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Added Candy Crush to Dashboard")
else:
    print("Could not find button")
