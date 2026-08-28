with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find('id="tvEffectPanel"')
print(html[idx:idx+1500])
