# -*- coding: utf-8 -*-
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

old_highlight = """                        document.querySelectorAll('.px-effect-btn').forEach(btn => {
                            if (btn.innerText.toLowerCase().includes(pxEffect.replace('_', ' ').split(' ')[0])) {
                                btn.classList.add('active');
                            } else if (pxEffect === 'solid' && btn.innerText.includes('Solid')) btn.classList.add('active');
                            else if (pxEffect === 'candy_crush' && btn.innerText.includes('Candy')) btn.classList.add('active');
                            else btn.classList.remove('active');
                        });"""

new_highlight = """                        document.querySelectorAll('.px-effect-btn').forEach(btn => {
                            // Check the onclick attribute to see if it matches exactly
                            const onclickStr = btn.getAttribute('onclick') || "";
                            if (onclickStr.includes(`'${pxEffect}'`) || onclickStr.includes(`"${pxEffect}"`)) {
                                btn.classList.add('active');
                            } else {
                                btn.classList.remove('active');
                            }
                        });"""

js = js.replace(old_highlight, new_highlight)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
print("JS fixed!")
