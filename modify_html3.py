# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

new_ui = """              <div class="panel-content" id="pxColorContent">
                    <div id="tetrisPaletteUI" style="display: none; margin-top: 12px; margin-bottom: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 11px; color: var(--subtext); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Tetris Custom Palette (Max 3)</div>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <div class="palette-slot" id="tslot0" style="width: 24px; height: 24px; border-radius: 50%; border: 1px dashed rgba(255,255,255,0.3);"></div>
                            <div class="palette-slot" id="tslot1" style="width: 24px; height: 24px; border-radius: 50%; border: 1px dashed rgba(255,255,255,0.3);"></div>
                            <div class="palette-slot" id="tslot2" style="width: 24px; height: 24px; border-radius: 50%; border: 1px dashed rgba(255,255,255,0.3);"></div>
                            <button onclick="clearTetrisPalette()" style="margin-left: auto; background: rgba(255,255,255,0.1); border: none; color: white; border-radius: 4px; padding: 4px 8px; font-size: 11px; cursor: pointer;">Clear Random</button>
                        </div>
                    </div>
                    <div class="color-grid" style="margin-top: 12px;">"""

html = re.sub(r'<div class="panel-content" id="pxColorContent">\s*<div class="color-grid" style="margin-top: 12px;">', new_ui, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("HTML injected for real!")
