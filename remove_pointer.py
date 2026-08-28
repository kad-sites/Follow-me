with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
js = re.sub(r'// Force range sliders to jump to click.*?\}\);\s*\}\);', '', js, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
