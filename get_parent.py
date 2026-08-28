with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

tab_c = 0
tab_t = 0
custom_p = 0

for i, line in enumerate(lines):
    if 'id="tab-corridor"' in line: tab_c = i
    if 'id="tab-tv"' in line: tab_t = i
    if 'id="customSeqPanel"' in line: custom_p = i

print(f"Corridor Tab starts at line {tab_c}")
print(f"TV Tab starts at line {tab_t}")
print(f"Custom Seq Panel starts at line {custom_p}")
