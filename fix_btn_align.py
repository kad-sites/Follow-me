with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

old = '<div id="saveBtnContainer" style="padding: 16px; padding-top: 0; padding-bottom: 24px;">'
new = '<div id="saveBtnContainer" style="margin-top: 8px; margin-bottom: 24px;">'

html = html.replace(old, new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
