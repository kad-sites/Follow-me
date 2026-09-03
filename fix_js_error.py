with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
js = re.sub(r'window\.savePxSettings = savePxSettings;\n', '', js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
