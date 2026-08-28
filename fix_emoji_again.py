with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("?? Pulse to Beat", "&#127925; Pulse to Beat")
html = html.replace("?? Volume Meter", "&#127925; Volume Meter")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
