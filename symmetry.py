import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_block = """        <div class="section" style="padding: 12px 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 11px; color: var(--subtext);">Pixels</span>
                    <input type="number" id="tvPixels" min="10" max="300" value="27" style="width: 52px; padding: 4px 6px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.15); background: rgba(0,0,0,0.3); color: #fff; font-size: 13px; font-family: monospace; text-align: center; -moz-appearance: textfield;">
                </div>
                <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 6px 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
                    ON
                </button>
            </div>
        </div>"""

new_block = """        <div class="section" style="padding: 8px 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 13px; font-weight: 500; color: var(--text);">Pixels</span>
                    <input type="number" id="tvPixels" min="10" max="300" value="27" style="width: 52px; height: 32px; padding: 0; border-radius: 6px; border: 1px solid rgba(255,255,255,0.15); background: rgba(0,0,0,0.3); color: #fff; font-size: 13px; font-weight: bold; font-family: inherit; text-align: center; -moz-appearance: textfield; box-sizing: border-box;">
                </div>
                <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; height: 32px; padding: 0 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s; box-sizing: border-box;">
                    ON
                </button>
            </div>
        </div>"""

html = html.replace(old_block, new_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
