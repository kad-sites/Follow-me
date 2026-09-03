# -*- coding: utf-8 -*-
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# Remove all 'let tetrisPalette = [];' from the very beginning
js = re.sub(r'let tetrisPalette = \[\];\n', '', js)

# Insert it safely AFTER import mqtt
js = js.replace("import mqtt from 'mqtt';", "import mqtt from 'mqtt';\nlet tetrisPalette = [];")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
print("Syntax fixed!")
