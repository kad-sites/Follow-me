with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# find setPxEffect block
js = re.sub(r'b\.innerHTML = b\.innerHTML\.replace\([^;]+;\n', '', js)
js = re.sub(r'btn\.innerHTML \+= [^;]+;\n', '', js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
