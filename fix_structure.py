with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's see the structure around tvEffectContent and customSeqPanel
import re

tv_effect_pattern = r'(<div class="section dropdown-panel" id="tvEffectPanel">.*?</div>\s*</div>\s*</div>)'
match = re.search(tv_effect_pattern, html, flags=re.DOTALL)
if match:
    print("Found tvEffectPanel")
    # Actually let's just print out the block
    # print(match.group(1))
