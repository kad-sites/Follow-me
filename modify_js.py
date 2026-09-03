# -*- coding: utf-8 -*-
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# Add tetris palette variables
js = "let tetrisPalette = [];\n" + js

# Update setPxColor
old_setPxColor = """            function setPxColor(btn, r, g, b) {
                document.querySelectorAll('.px-color-btn').forEach(b => b.classList.remove('active'));
                if(btn) btn.classList.add('active');
                pxR = r; pxG = g; pxB = b;
                updateGradient(document.getElementById('pxBrightness'), r, g, b);
                sendPxUpdate();
            }"""

new_setPxColor = """            function clearTetrisPalette() {
                tetrisPalette = [];
                updateTetrisUI();
                sendPxUpdate();
            }
            
            function updateTetrisUI() {
                for (let i = 0; i < 3; i++) {
                    let slot = document.getElementById('tslot' + i);
                    if (i < tetrisPalette.length) {
                        slot.style.background = `rgb(${tetrisPalette[i].r}, ${tetrisPalette[i].g}, ${tetrisPalette[i].b})`;
                        slot.style.border = 'none';
                    } else {
                        slot.style.background = 'transparent';
                        slot.style.border = '1px dashed rgba(255,255,255,0.3)';
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
                    return; // Don't highlight color button for solid color
                }
                
                document.querySelectorAll('.px-color-btn').forEach(b => b.classList.remove('active'));
                if(btn) btn.classList.add('active');
                pxR = r; pxG = g; pxB = b;
                updateGradient(document.getElementById('pxBrightness'), r, g, b);
                sendPxUpdate();
            }"""

js = js.replace(old_setPxColor, new_setPxColor)

# Update setPxRandomColor
old_rand = """            function setPxRandomColor() {
                document.querySelectorAll('.px-color-btn').forEach(b => b.classList.remove('active'));
                let r = Math.floor(Math.random() * 256);
                let g = Math.floor(Math.random() * 256);
                let b = Math.floor(Math.random() * 256);
                pxR = r; pxG = g; pxB = b;
                updateGradient(document.getElementById('pxBrightness'), r, g, b);
                sendPxUpdate();
            }"""
new_rand = """            function setPxRandomColor() {
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
js = js.replace(old_rand, new_rand)

# Show/hide UI in setPxEffect
old_setPxEffect = """            function setPxEffect(btn, effect) {
                document.querySelectorAll('.px-effect-btn').forEach(b => {
                    b.classList.remove('active');
                                  });
                btn.classList.add('active');
                              pxEffect = effect;
                sendPxUpdate();
            }"""

new_setPxEffect = """            function setPxEffect(btn, effect) {
                document.querySelectorAll('.px-effect-btn').forEach(b => {
                    b.classList.remove('active');
                                  });
                btn.classList.add('active');
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
js = js.replace(old_setPxEffect, new_setPxEffect)

# Pack the payload in sendPxUpdate
old_payload = """                let payload = {
                    power: pxIsOn,
                    brightness: parseInt(document.getElementById('pxBrightness').value),
                    speed: parseInt(document.getElementById('pxSpeed').value),
                    effect: pxEffect, // 'pacman'
                    text: pxText,
                    r: pxR,
                    g: pxG,
                    b: pxB
                };"""

new_payload = """                let tetHex = tetrisPalette.map(c => (c.r << 16) | (c.g << 8) | c.b);
                let payload = {
                    power: pxIsOn,
                    brightness: parseInt(document.getElementById('pxBrightness').value),
                    speed: parseInt(document.getElementById('pxSpeed').value),
                    effect: pxEffect, // 'pacman'
                    text: pxText,
                    r: pxR,
                    g: pxG,
                    b: pxB,
                    tColors: tetHex
                };"""
js = js.replace(old_payload, new_payload)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
print("JS updated!")
