import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_css = """        .section-title {
            font-size: 15px;
            font-weight: 600;
        }"""

new_css = """        .section-title {
            font-size: 13.5px;
            font-weight: 600;
        }"""

html = html.replace(old_css, new_css)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
