# -*- coding: utf-8 -*-
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

js = js.replace("let tetrisPalette = [];\nimport mqtt from 'mqtt';", "import mqtt from 'mqtt';\nlet tetrisPalette = [];")

# Also, since I did this twice (maybe?), let's make sure
js = re.sub(r'^(let tetrisPalette = \[\];\n)+import mqtt', r"import mqtt", js)
js = js.replace("import mqtt from 'mqtt';", "import mqtt from 'mqtt';\nlet tetrisPalette = [];")

# Wait, let's just do it carefully.
