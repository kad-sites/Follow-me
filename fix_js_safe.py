# -*- coding: utf-8 -*-
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# Insert variable at top
if "let tetrisPalette" not in js:
    js = js.replace("import mqtt from 'mqtt';", "import mqtt from 'mqtt';\nlet tetrisPalette = [];")

# 1. setPxEffect
old_eff = """            function setPxEffect(btn, effect) {
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
                    if (content.style.maxHeight) {
                        content.style.maxHeight = content.scrollHeight + 50 + "px";
                    }
                }
                
                sendPxUpdate();
            }"""

# Actually, if I already pushed `modify_js.py` to git, maybe `git restore` restored the broken version!
# Let me check git log!
