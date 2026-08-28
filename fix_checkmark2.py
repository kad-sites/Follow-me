import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace ? with unicode checkmark for CSS
pattern = r"content:\s*'\?';"
html = re.sub(pattern, r"content: '\\2713';", html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
