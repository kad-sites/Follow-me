import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

save_btn = """
      <div id="saveBtnContainer" style="display: none; padding: 16px; padding-top: 0; padding-bottom: 24px;">
          <button onclick="saveTvSettings()" style="width: 100%; background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 12px; font-size: 14px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
              ?? Save Settings to Device
          </button>
      </div>
  </main>"""

html = re.sub(r'</main>', save_btn, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
