import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Pull White Temperature OUT of tvColorContent so it NEVER hides
# Find tvColorContent end and move it up before the White Temperature divider
pattern = r'(<div class="color-grid".*?</div>)(\s*<div style="height: 1px; background: rgba\(255,255,255,0\.05\); margin: 4px 0;"></div>\s*<div class="section-header">\s*<div class="section-title">White Temperature</div>.*?</label>\s*</div>\s*</div>\s*</div>)'
# wait, the white temperature block ends with slider-container </div>
# Let's find exactly the block to move out.
