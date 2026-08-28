import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the entire TV Power + Pixels block
old_block = """            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="section-title" style="margin-bottom: 0;">TV Power</div>
                <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 6px 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
                    ON
                </button>
            </div>
            </div>
                <div class="section-header" style="margin-top: 8px;">
                    <div class="section-title">TV Pixels</div>
                    <div class="value-display" id="tvPixelsVal">27</div>
                </div>
                <div class="slider-container">
                    <input type="range" id="tvPixels" min="10" max="300" value="27" style="touch-action: pan-y;">
                </div>"""

new_block = """            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 11px; color: var(--subtext);">Pixels</span>
                    <input type="number" id="tvPixels" min="10" max="300" value="27" style="width: 52px; padding: 4px 6px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.15); background: rgba(0,0,0,0.3); color: #fff; font-size: 13px; font-family: monospace; text-align: center; -moz-appearance: textfield;">
                </div>
                <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 6px 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
                    ON
                </button>
            </div>"""

html = html.replace(old_block, new_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
