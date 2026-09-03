# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("\\'fireworks\\'", "'fireworks'")
html = html.replace('\\">Fireworks', '">Fireworks')
html = html.replace("\\'vu_meter\\'", "'vu_meter'")
html = html.replace('\\">VU Meter', '">VU Meter')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
