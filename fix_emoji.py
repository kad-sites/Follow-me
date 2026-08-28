with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("?? Save Settings to Device", "Save Settings to Device")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
