import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove FOUC header logic
html_pattern = r'const headerTitle = document\.querySelector\(\'\.header \.title\'\);\s*if \(headerTitle\) \{.*?\n\s*\}'
html = re.sub(html_pattern, '', html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
