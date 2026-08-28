with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
js = js.replace('client.publish("kad/tvbacklit/cmd",', 'client.publish("kad/tvbacklit/cmd/zoheb",')

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
