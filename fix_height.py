# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("max-height: 500px;", "max-height: 1000px;")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
