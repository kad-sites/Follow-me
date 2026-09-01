with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "nav-tabs" in line or "Corridor" in line or "TV Backlight" in line:
        print(f"{i}: {line.strip()}")
