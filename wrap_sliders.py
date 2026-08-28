with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
pattern = r"(sliders\.forEach\(s => \{\s*)s\.el\.addEventListener\('input', \(\) => \{(.*?)\}\);\s*\}\);"
replacement = r"\1if (s.el) {\n                s.el.addEventListener('input', () => {\2});\n            }\n        });"

js = re.sub(pattern, replacement, js, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
