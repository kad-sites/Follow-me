with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('    <div class="toast" id="toast">', '    </div>\n    <div class="toast" id="toast">')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
