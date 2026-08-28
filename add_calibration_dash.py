import re

with open('index.html', 'r') as f:
    html = f.read()

calibration_section = '''    <!-- Calibration Settings -->
    <div class="section">
        <div class="section-header" style="justify-content: space-between; margin-bottom: 0; cursor: pointer; padding: 4px 0;" onclick="toggleCalib()">
            <div class="section-title">Calibration (Fix Alignment)</div>
            <div id="calibArrow" style="color: var(--subtext); font-size: 12px;">?</div>
        </div>
        
        <div id="calibPanel" style="display: none; margin-top: 16px;">
            <div class="section-header">
                <div class="section-title" style="font-size: 13px; font-weight: 500;">LED Density</div>
                <div class="value-display" id="densityVal">60 LEDs/m</div>
            </div>
            <div class="slider-container" style="margin-bottom: 4px;">
                <input type="range" style="touch-action: pan-y;" id="ledDensity" min="10" max="144" value="60">
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 10px; color: var(--subtext); margin-bottom: 12px;">
                <span>30/m</span><span>144/m</span>
            </div>

            <div class="section-header">
                <div class="section-title" style="font-size: 13px; font-weight: 500;">Sensor Offset</div>
                <div class="value-display" id="offsetVal">0 cm</div>
            </div>
            <div class="slider-container" style="margin-bottom: 4px;">
                <input type="range" style="touch-action: pan-y;" id="sensorOffset" min="-200" max="200" value="0">
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 10px; color: var(--subtext); margin-bottom: 12px;">
                <span>-200cm</span><span>+200cm</span>
            </div>
        </div>
    </div>

    <!-- Radar Settings -->'''

html = html.replace('    <!-- Radar Settings -->', calibration_section)

# JS toggle function
toggle_js = '''        function toggleRadar() {
            const panel = document.getElementById('radarPanel');
            const arrow = document.getElementById('radarArrow');
            if(panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '?';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '?';
            }
        }
        function toggleCalib() {
            const panel = document.getElementById('calibPanel');
            const arrow = document.getElementById('calibArrow');
            if(panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '?';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '?';
            }
        }'''

html = html.replace('        function toggleRadar() {\n            const panel = document.getElementById(\'radarPanel\');\n            const arrow = document.getElementById(\'radarArrow\');\n            if(panel.style.display === \'none\') {\n                panel.style.display = \'block\';\n                arrow.innerHTML = \'?\';\n            } else {\n                panel.style.display = \'none\';\n                arrow.innerHTML = \'?\';\n            }\n        }', toggle_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
