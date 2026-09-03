with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
js = js.replace("let TOPIC_STATUS, TOPIC_RADAR, TOPIC_CMD;", "let TOPIC_STATUS, TOPIC_RADAR, TOPIC_CMD;\nlet TOPIC_PX_CMD = 'kad/pixora/cmd/zoheb';\nlet TOPIC_PX_STATUS = 'kad/pixora/status/zoheb';\n")

# Subscribe to Pixora status
js = js.replace('client.subscribe("kad/tvbacklit/cmd/zoheb");', 'client.subscribe("kad/tvbacklit/cmd/zoheb");\n            client.subscribe(TOPIC_PX_STATUS);\n')

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
