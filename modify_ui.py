import re

# ------------- INDEX.HTML -------------
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Sleeker layout via CSS tweaks
html = html.replace('.section {', '.section { margin-bottom: 12px; padding: 12px 16px; ') # add smaller padding
html = re.sub(r'padding: 16px 20px;', 'padding: 12px 16px;', html) # remove old padding if it exists
html = html.replace('.section-header {\n            display: flex;', '.section-header {\n            display: flex;\n            margin-bottom: 8px;')
html = re.sub(r'margin-bottom: 16px;', 'margin-bottom: 8px;', html) # Replace generic 16px bottom margins with 8px

# 2. Make Color Mode collapsible
color_section_old = '''    <!-- Color Section -->
    <div class="section">
        <div class="section-header">
            <div class="section-title">Color Mode</div>
        </div>
        
        <!-- Target Selection Tabs -->'''

color_section_new = '''    <!-- Color Section -->
    <div class="section">
        <div class="section-header" style="justify-content: space-between; margin-bottom: 0; cursor: pointer; padding: 4px 0;" onclick="toggleColor()">
            <div class="section-title">Color Mode</div>
            <div id="colorArrow" style="color: var(--subtext); font-size: 12px;">&#9660;</div>
        </div>
        
        <div id="colorPanel" style="display: none; margin-top: 12px;">
            <!-- Target Selection Tabs -->'''

html = html.replace(color_section_old, color_section_new)
html = html.replace('        </div>\n    </div>\n\n    <!-- Calibration Settings -->', '        </div>\n        </div>\n    </div>\n\n    <!-- Calibration Settings -->')

# 3. Add Apply Button for Main Settings
apply_btn_html = '''        <button class="btn" style="background: var(--accent); color: white; margin-top: 16px;" onclick="applyMainSettings()">Apply Slider Settings</button>
    </div>

    <!-- Calibration Settings -->'''
html = html.replace('    </div>\n\n    <!-- Calibration Settings -->', apply_btn_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# ------------- MAIN.JS -------------
with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Remove auto-update from slider drag
js = js.replace('throttledUpdate({ [s.key]: parseInt(s.el.value) });', '// throttledUpdate removed - waiting for Apply button')

# 2. Add applyMainSettings
apply_func = '''        function applyMainSettings() {
            const payload = {};
            sliders.forEach(s => {
                if (s.el) payload[s.key] = parseInt(s.el.value);
            });
            sendUpdate(payload);
            showToast("Settings Applied to ESP32");
        }
        window.applyMainSettings = applyMainSettings;
'''
js = js.replace('window.applyRadarSettings = applyRadarSettings;', apply_func + '\n        window.applyRadarSettings = applyRadarSettings;')

# 3. Add toggleColor
toggle_color_func = '''        function toggleColor() {
            const panel = document.getElementById('colorPanel');
            const arrow = document.getElementById('colorArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '&#9650;';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '&#9660;';
            }
        }
'''
js = js.replace('window.toggleRadar = toggleRadar;', toggle_color_func + '\n        window.toggleRadar = toggleRadar;\n        window.toggleColor = toggleColor;')

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
