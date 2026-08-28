import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Change max of cDel to 3000
html = html.replace('id="cDel" min="50" max="2000"', 'id="cDel" min="50" max="3000"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
