with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
# Find the start of tab-tv and end of the duplicated tvBrightness section
start_str = '<div id="tab-tv" class="tab-content" style="display: none;">'
end_str = '<div class="section dropdown-panel" id="tvColorPanel">'

before = html.split(start_str)[0]
after = html.split(end_str)[1]

new_middle = """
        <!-- Power Button -->
        <div class="section" style="display: flex; justify-content: center; padding: 12px; margin-bottom: 8px;">
            <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 12px 24px; font-size: 16px; font-weight: bold; width: 100%; cursor: pointer; transition: all 0.2s;">
                TURN OFF
            </button>
        </div>

        <div class="section">
            <div class="section-header">
                <div class="section-title">TV Brightness</div>
                <div class="value-display" id="tvBrightVal">12%</div>
            </div>
            <div class="slider-container">
                <input type="range" id="tvBrightness" min="0" max="255" value="30" style="touch-action: pan-y;">
            </div>

            <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>

            <div class="section-header">
                <div class="section-title">Effect Speed</div>
                <div class="value-display" id="tvSpeedVal">50%</div>
            </div>
            <div class="slider-container">
                <input type="range" id="tvSpeed" min="1" max="100" value="50" style="touch-action: pan-y;">
            </div>
        </div>
"""

html = before + start_str + new_middle + '\n        ' + end_str + after

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
