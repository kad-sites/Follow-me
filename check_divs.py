with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

def find_div_ends(html, div_id):
    start_idx = html.find(f'id="{div_id}"')
    if start_idx == -1: return -1
    
    # backtrack to '<'
    while html[start_idx] != '<':
        start_idx -= 1
        
    depth = 0
    i = start_idx
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+5] == '</div':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1

corridor_end = find_div_ends(html, "tab-corridor")
tv_end = find_div_ends(html, "tab-tv")
custom_start = html.find('id="customSeqPanel"')

print(f"Corridor ends at char {corridor_end}")
print(f"TV ends at char {tv_end}")
print(f"Custom seq starts at char {custom_start}")
