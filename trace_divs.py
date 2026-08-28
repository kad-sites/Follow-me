with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

tv_start = html.find('id="tab-tv"')
while html[tv_start] != '<': tv_start -= 1

print(html[tv_start:tv_start+1000])
