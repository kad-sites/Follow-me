with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace CSS rule
html = html.replace('margin-bottom: 24px; /* Two line gap from header */', 'margin-bottom: 8px;')

# Replace inline style
html = html.replace('margin: 0 auto 24px auto;', 'margin: 0 auto 8px auto;')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
