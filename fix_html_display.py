# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('<div id="tab-pixora" class="tab-content" style="display: block;">', '<div id="tab-pixora" class="tab-content" style="display: none;">')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("HTML display fixed!")
