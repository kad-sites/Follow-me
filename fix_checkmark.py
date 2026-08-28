import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the question mark with a checkmark
pattern = r"content:\s*'\?';"
html = re.sub(pattern, "content: '?';", html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
