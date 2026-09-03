with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
js = js.replace("document.getElementById('connErrorMsg').style.display = 'block';", "const err = document.getElementById('connErrorMsg');\n            if (err) err.style.display = 'block';")

js = js.replace("const client = mqtt.connect('wss://broker.hivemq.com:8884/mqtt');", "const client = mqtt.connect('wss://broker.hivemq.com:8884/mqtt', { clientId: 'followme_web_' + Math.random().toString(16).substr(2, 8) });")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
