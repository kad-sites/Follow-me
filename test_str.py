with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("End comment:", html.find("<!-- End tab-tv -->"))
