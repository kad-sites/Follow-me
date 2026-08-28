import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make TV Color content open by default
html = html.replace('<div class="panel-content" id="tvColorContent">', '<div class="panel-content open" id="tvColorContent">')

# Make the chevron point up for TV Color
html = html.replace('<svg id="tvColorChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s;">', '<svg id="tvColorChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s; transform: rotate(180deg);">')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
