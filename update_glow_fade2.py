import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_str = "#glowSize::-webkit-slider-runnable-track { background: linear-gradient(to right, #333 0%, #333 ${leftEdge}%, ${baseColorHex} ${leftEdge}%, ${baseColorHex} ${rightEdge}%, #333 ${rightEdge}%, #333 100%) !important; }"

new_str = "#glowSize::-webkit-slider-runnable-track { background: linear-gradient(to right, #333 0%, #333 ${leftEdge}%, ${baseColorHex} 50%, #333 ${rightEdge}%, #333 100%) !important; }"

js = js.replace(old_str, new_str)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
