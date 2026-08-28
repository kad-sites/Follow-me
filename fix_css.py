with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('input[type=range] {', 'input[type=range] {\n            pointer-events: none;')
html = html.replace('input[type=range]::-webkit-slider-thumb {', 'input[type=range]::-webkit-slider-thumb {\n            pointer-events: auto;')
html = html.replace('input[type=range]::-moz-range-thumb {', 'input[type=range]::-moz-range-thumb {\n            pointer-events: auto;')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
