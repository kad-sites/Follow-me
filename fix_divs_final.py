import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Currently, the end of tab-tv looks like this:
#     </div>
#     
#         <div class="section" id="customSeqPanel" ...>
#             ...
#         </div>
# 
#     <div class="toast" id="toast">Settings Saved</div>

# Find everything from <div class="section" id="customSeqPanel" down to the closing </div> before <div class="toast"
pattern = r'(\s*</div>)\s*(<div class="section" id="customSeqPanel".*?</div>)\s*<div class="toast"'
match = re.search(pattern, html, flags=re.DOTALL)
if match:
    closing_div = match.group(1) # The closing div of tab-tv
    custom_panel = match.group(2) # The custom seq panel
    
    # We want to put custom_panel BEFORE the closing_div of tab-tv
    new_html = custom_panel + "\n" + closing_div + "\n\n    <div class=\"toast\""
    html = html[:match.start()] + new_html + html[match.end():]
else:
    print("Match failed. Using a different approach.")
    # The structure might actually be:
    #     <div id="saveBtnContainer" ...>
    #     </div>
    # </div> <!-- End tab-tv -->
    # 
    # <div class="section" id="customSeqPanel" ...>
    # ...
    # </div>

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
