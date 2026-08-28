import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# I will find the entire TV Power section down to the slider-container of TV Pixels
pattern = r'(<div class="section-title"[^>]*>TV Power</div>.*?</button>\s*</div>)\s*</div>\s*<div class="section-header"[^>]*>\s*<div class="section-title">TV Pixels</div>\s*<div class="value-display"[^>]*>.*?</div>\s*</div>\s*<div class="slider-container">\s*<input type="range" id="tvPixels".*?>\s*</div>'

new_block = """            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 11px; color: var(--subtext);">Pixels</span>
                    <input type="number" id="tvPixels" min="10" max="300" value="27" style="width: 52px; padding: 4px 6px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.15); background: rgba(0,0,0,0.3); color: #fff; font-size: 13px; font-family: monospace; text-align: center; -moz-appearance: textfield;">
                </div>
                <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 6px 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
                    ON
                </button>
            </div>
            </div>"""

# Test if pattern matches
match = re.search(pattern, html, flags=re.DOTALL)
if match:
    print("Match found! Replacing...")
    html = re.sub(pattern, new_block, html, flags=re.DOTALL)
else:
    print("NO MATCH! Let me try a simpler pattern.")
    # Try finding just TV Power to the end of TV Pixels slider
    pattern2 = r'<div class="section-title"[^>]*>TV Power</div>.*?</button>\s*</div>\s*</div>\s*<div class="section-header"[^>]*>\s*<div class="section-title">TV Pixels</div>.*?<input type="range" id="tvPixels".*?>\s*</div>'
    match2 = re.search(pattern2, html, flags=re.DOTALL)
    if match2:
        print("Simpler pattern matched! Replacing...")
        html = re.sub(pattern2, new_block, html, flags=re.DOTALL)
    else:
        print("FAILED AGAIN.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
