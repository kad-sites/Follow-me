import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace TV Power section with the new inline block
power_pattern = r'<div class="section-title" style="margin-bottom: 0;">TV Power</div>'
new_power = """<div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 11px; color: var(--subtext);">Pixels</span>
                    <input type="number" id="tvPixels" min="10" max="300" value="27" style="width: 52px; padding: 4px 6px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.15); background: rgba(0,0,0,0.3); color: #fff; font-size: 13px; font-family: monospace; text-align: center; -moz-appearance: textfield;">
                </div>"""
html = re.sub(power_pattern, new_power, html)

# 2. Delete the old TV Pixels slider section
pixels_pattern = r'<div class="section-header" style="margin-top: 8px;">\s*<div class="section-title">TV Pixels</div>\s*<div class="value-display" id="tvPixelsVal">.*?</div>\s*</div>\s*<div class="slider-container">\s*<input type="range" id="tvPixels".*?>\s*</div>'
html = re.sub(pixels_pattern, '', html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
