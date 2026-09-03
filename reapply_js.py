# -*- coding: utf-8 -*-
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# 1. Update sendPxUpdate
old_pay = r'let payload = \{\s*power: pxIsOn,\s*brightness: parseInt\(document\.getElementById\(\'pxBrightness\'\) \? document\.getElementById\(\'pxBrightness\'\)\.value : 60\),\s*speed: parseInt\(document\.getElementById\(\'pxSpeed\'\) \? document\.getElementById\(\'pxSpeed\'\)\.value : 50\),\s*effect: pxEffect,\s*text: pxText,\s*r: pxR,\s*g: pxG,\s*b: pxB\s*\};'
new_pay = """let tetHex = tetrisPalette.map(c => (c.r << 16) | (c.g << 8) | c.b);
                    let payload = {
                        power: pxIsOn,
                        brightness: parseInt(document.getElementById('pxBrightness') ? document.getElementById('pxBrightness').value : 60),
                        speed: parseInt(document.getElementById('pxSpeed') ? document.getElementById('pxSpeed').value : 50),
                        effect: pxEffect,
                        text: pxText,
                        r: pxR,
                        g: pxG,
                        b: pxB,
                        tColors: tetHex
                    };"""
js = re.sub(old_pay, new_pay, js)


# 2. Update setPxEffect
old_eff = r'function setPxEffect\(btn, effect\) \{\s*document\.querySelectorAll\(\'\.px-effect-btn\'\)\.forEach\(b => \{\s*b\.classList\.remove\(\'active\'\);\s*\}\);\s*if\(btn\) btn\.classList\.add\(\'active\'\);\s*pxEffect = effect;\s*sendPxUpdate\(\);\s*\}'
new_eff = """function setPxEffect(btn, effect) {
                document.querySelectorAll('.px-effect-btn').forEach(b => {
                    b.classList.remove('active');
                });
                if(btn) btn.classList.add('active');
                pxEffect = effect;
                
                let tetUI = document.getElementById('tetrisPaletteUI');
                if (tetUI) {
                    tetUI.style.display = (effect === 'tetris') ? 'block' : 'none';
                    let content = document.getElementById('pxColorContent');
                    if (content && content.style.maxHeight) {
                        content.style.maxHeight = content.scrollHeight + 50 + "px";
                    }
                }
                
                sendPxUpdate();
            }"""
js = re.sub(old_eff, new_eff, js)


# 3. Update setPxColor
old_col = r'function setPxColor\(btn, r, g, b\) \{\s*document\.querySelectorAll\(\'\.px-color-btn\'\)\.forEach\(b => b\.classList\.remove\(\'active\'\)\);\s*if\(btn\) btn\.classList\.add\(\'active\'\);\s*pxR = r; pxG = g; pxB = b;\s*updateGradient\(document\.getElementById\(\'pxBrightness\'\), r, g, b\);\s*sendPxUpdate\(\);\s*\}'
new_col = """function clearTetrisPalette() {
                tetrisPalette = [];
                updateTetrisUI();
                sendPxUpdate();
            }
            
            function updateTetrisUI() {
                for (let i = 0; i < 3; i++) {
                    let slot = document.getElementById('tslot' + i);
                    if (slot) {
                        if (i < tetrisPalette.length) {
                            slot.style.background = `rgb(${tetrisPalette[i].r}, ${tetrisPalette[i].g}, ${tetrisPalette[i].b})`;
                            slot.style.border = 'none';
                        } else {
                            slot.style.background = 'transparent';
                            slot.style.border = '1px dashed rgba(255,255,255,0.3)';
                        }
                    }
                }
            }

            function setPxColor(btn, r, g, b) {
                if (pxEffect === 'tetris') {
                    if (tetrisPalette.length < 3) {
                        tetrisPalette.push({r, g, b});
                        updateTetrisUI();
                        sendPxUpdate();
                    }
                    return;
                }
                
                document.querySelectorAll('.px-color-btn').forEach(b => b.classList.remove('active'));
                if(btn) btn.classList.add('active');
                pxR = r; pxG = g; pxB = b;
                updateGradient(document.getElementById('pxBrightness'), r, g, b);
                sendPxUpdate();
            }"""
js = re.sub(old_col, new_col, js)


# 4. Update setPxRandomColor
old_rand = r'function setPxRandomColor\(\) \{\s*document\.querySelectorAll\(\'\.px-color-btn\'\)\.forEach\(b => b\.classList\.remove\(\'active\'\)\);\s*let r = Math\.floor\(Math\.random\(\) \* 256\);\s*let g = Math\.floor\(Math\.random\(\) \* 256\);\s*let b = Math\.floor\(Math\.random\(\) \* 256\);\s*pxR = r; pxG = g; pxB = b;\s*updateGradient\(document\.getElementById\(\'pxBrightness\'\), r, g, b\);\s*sendPxUpdate\(\);\s*\}'
new_rand = """function setPxRandomColor() {
                let r = Math.floor(Math.random() * 256);
                let g = Math.floor(Math.random() * 256);
                let b = Math.floor(Math.random() * 256);
                if (pxEffect === 'tetris') {
                    if (tetrisPalette.length < 3) {
                        tetrisPalette.push({r, g, b});
                        updateTetrisUI();
                        sendPxUpdate();
                    }
                    return;
                }
                document.querySelectorAll('.px-color-btn').forEach(btn => btn.classList.remove('active'));
                pxR = r; pxG = g; pxB = b;
                updateGradient(document.getElementById('pxBrightness'), r, g, b);
                sendPxUpdate();
            }"""
js = re.sub(old_rand, new_rand, js)


# Export clearTetrisPalette
js = js.replace("window.setPxEffect = setPxEffect;", "window.setPxEffect = setPxEffect;\n            window.clearTetrisPalette = clearTetrisPalette;")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
print("JS updated safely!")
