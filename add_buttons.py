# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_buttons = """                    <button class="px-effect-btn" onclick="setPxEffect('candy_crush')">
                        <span class="icon">🍬</span>
                        Candy Crush
                    </button>
                </div>"""

new_buttons = """                    <button class="px-effect-btn" onclick="setPxEffect('candy_crush')">
                        <span class="icon">🍬</span>
                        Candy Crush
                    </button>
                    <button class="px-effect-btn" onclick="setPxEffect('fireworks')">
                        <span class="icon">🎆</span>
                        Fireworks
                    </button>
                    <button class="px-effect-btn" onclick="setPxEffect('vu_meter')">
                        <span class="icon">🎚️</span>
                        VU Meter
                    </button>
                </div>"""

if old_buttons in html:
    html = html.replace(old_buttons, new_buttons)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Buttons added to dashboard!")
else:
    print("Could not find old_buttons")
