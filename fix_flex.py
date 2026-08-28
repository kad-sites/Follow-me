import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

pattern = r'(\.tv-effect-btn\s*\{.*?)(text-align:\s*left;)'
repl = r'\1display: flex; justify-content: space-between; align-items: center;'
html = re.sub(pattern, repl, html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
