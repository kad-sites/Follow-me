with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('?', '&#9660;').replace('?', '&#9650;')
# Replace any corrupted ones too just in case
html = html.replace('?</div>', '&#9660;</div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
