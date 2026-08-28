import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make section padding even smaller
html = re.sub(r'(\.section\s*\{[^}]*)padding:\s*10px\s*16px;', r'\1padding: 6px 12px;', html)
html = re.sub(r'(\.section\s*\{[^}]*)margin-bottom:\s*8px;', r'\1margin-bottom: 4px;', html)

# Make panel header padding smaller (for the dropdowns)
html = re.sub(r'(\.panel-header\s*\{[^}]*)padding:\s*10px\s*16px;', r'\1padding: 6px 12px;', html)

# Make the empty div space smaller
html = html.replace('margin: 8px 0;', 'margin: 4px 0;')
html = html.replace('margin-top: 8px;', 'margin-top: 4px;')
html = html.replace('gap: 4px;', 'gap: 2px;') # effect buttons

# Slightly reduce the section title margin
html = re.sub(r'(\.section-header\s*\{[^}]*)margin-bottom:\s*4px;', r'\1margin-bottom: 2px;', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
