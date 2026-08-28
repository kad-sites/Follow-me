import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# We need to replace the old glowSize linear gradient
old_pattern = r"#glowSize::-webkit-slider-runnable-track \{ background: linear-gradient\(to right, #333 0%, #333 \${leftEdge}%, \${baseColorHex} \${leftEdge}%, \${baseColorHex} \${rightEdge}%, #333 \${rightEdge}%, #333 100%\) !important; \}"

new_pattern = r"#glowSize::-webkit-slider-runnable-track { background: linear-gradient(to right, #333 0%, #333 ${leftEdge}%, ${baseColorHex} 50%, #333 ${rightEdge}%, #333 100%) !important; }"

js = js.replace(old_pattern, new_pattern)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
