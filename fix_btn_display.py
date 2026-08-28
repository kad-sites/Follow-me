import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Instead of putting it outside the tab, put it INSIDE the tab-tv div at the end
old_html = """      </div> <!-- End tab-tv -->
      
      <div id="saveBtnContainer" style="display: none; padding: 16px; padding-top: 0; padding-bottom: 24px;">
          <button onclick="saveTvSettings()" style="width: 100%; background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 12px; font-size: 14px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
              ?? Save Settings to Device
          </button>
      </div>"""

new_html = """          <div id="saveBtnContainer" style="padding: 16px; padding-top: 0; padding-bottom: 24px;">
              <button onclick="saveTvSettings()" style="width: 100%; background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 12px; font-size: 14px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
                  ?? Save Settings to Device
              </button>
          </div>
      </div> <!-- End tab-tv -->"""

html = html.replace(old_html, new_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
