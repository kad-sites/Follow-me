# -*- coding: utf-8 -*-
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

old_eff = r'function setPxEffect\(btn,\s*effect\)\s*\{[\s\S]*?pxEffect\s*=\s*effect;\s*sendPxUpdate\(\);\s*\}'
new_eff = """function setPxEffect(btn, effect) {
                document.querySelectorAll('.px-effect-btn').forEach(b => {
                    b.classList.remove('active');
                });
                if(btn) btn.classList.add('active');
                pxEffect = effect;
                
                // Show tetris custom UI if tetris is selected
                let tetUI = document.getElementById('tetrisPaletteUI');
                if (tetUI) {
                    tetUI.style.display = (effect === 'tetris') ? 'block' : 'none';
                    // Recompute max-height if the dropdown is open
                    let content = document.getElementById('pxColorContent');
                    if (content && content.style.maxHeight) {
                        content.style.maxHeight = content.scrollHeight + 50 + "px";
                    }
                }
                
                sendPxUpdate();
            }"""

js = re.sub(old_eff, new_eff, js)

# We also need to add clearTetrisPalette() to the global window object so the HTML button can call it!
if "window.clearTetrisPalette = clearTetrisPalette;" not in js:
    js = js.replace("window.setPxEffect = setPxEffect;", "window.setPxEffect = setPxEffect;\n          window.clearTetrisPalette = clearTetrisPalette;")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
print("setPxEffect fixed!")
