import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix CSS padding for tv-effect-btn
pattern_css = r'(\.tv-effect-btn\s*\{[^}]*)padding:\s*12px;'
repl_css = r'\1padding: 8px 12px;'
html = re.sub(pattern_css, repl_css, html)

# 2. Fix the HTML gap for the list
pattern_html = r'<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 12px;">'
repl_html = r'<div style="display: flex; flex-direction: column; gap: 4px; margin-top: 8px;">'
html = html.replace(pattern_html, repl_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
