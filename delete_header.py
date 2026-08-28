import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove the header HTML block
header_pattern = r'<div class="header".*?</div>\s*</div>'
html = re.sub(header_pattern, '', html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Remove the dynamic header logic from main.js
js_pattern = r'const headerTitle = document\.querySelector\(\'\.header \.title\'\);\s*if \(headerTitle\) \{.*?\n\s*\}'
js = re.sub(js_pattern, '', js, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
