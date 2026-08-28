import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I will replace all instances of arrow.innerText = '...' with innerHTML
js = re.sub(r"arrow\.innerText\s*=\s*'[^']*';", "arrow.innerHTML = '&#9660;';", js)
# Now fix the ones that should be UP
js = js.replace("panel.style.display = 'block';\n                arrow.innerHTML = '&#9660;';", "panel.style.display = 'block';\n                arrow.innerHTML = '&#9650;';")

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
