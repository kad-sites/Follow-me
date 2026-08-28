import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add a Save button at the bottom of the TV Effect dropdown/panel area
save_btn = """              </div> <!-- End of customSeqPanel -->
              
              <div style="padding-top: 16px;">
                  <button id="saveTvBtn" onclick="saveTvSettings()" style="width: 100%; background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 12px; font-size: 14px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
                      ?? Save Settings to Device
                  </button>
              </div>

          </div> <!-- End of tvEffectContent -->"""

html = html.replace("</div> <!-- End of customSeqPanel -->\n          </div>", save_btn)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
