# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("\\'pacman\\'", "'pacman'")
html = html.replace("\\'falling_sand\\'", "'falling_sand'")
html = html.replace("\\'smart_snake\\'", "'smart_snake'")
html = html.replace("\\'warp_speed\\'", "'warp_speed'")
html = html.replace("\\'rain_ripples\\'", "'rain_ripples'")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
