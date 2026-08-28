import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# The TV tab html
tv_tab_html = """
    </div>

    <!-- TAB 2: TV BACKLIGHT -->
    <div id="tab-tv" class="tab-content" style="display: none;">
        <div class="section">
            <div class="section-header">
                <div class="section-title">TV Brightness</div>
                <div class="value-display" id="tvBrightVal">100%</div>
            </div>
            <div class="slider-container">
                <input type="range" id="tvBrightness" min="0" max="255" value="255" style="touch-action: pan-y;">
            </div>
        </div>

        <div class="section dropdown-panel" id="tvColorPanel">
            <div class="panel-header" onclick="toggleTvColor()">
                <div class="section-title" style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                    <span>TV Color</span>
                    <svg id="tvColorChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s;">
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                </div>
            </div>
            <div class="panel-content" id="tvColorContent">
                <div class="color-grid" style="margin-top: 12px;">
                    <!-- Warm/Whites -->
                    <button class="color-btn tv-color-btn active" data-r="255" data-g="147" data-b="41" onclick="setTvColor(this, 255, 147, 41)">
                        <div class="color-swatch" style="background: rgb(255,147,41)"></div>
                    </button>
                    <button class="color-btn tv-color-btn" data-r="255" data-g="214" data-b="170" onclick="setTvColor(this, 255, 214, 170)">
                        <div class="color-swatch" style="background: rgb(255,214,170)"></div>
                    </button>
                    <button class="color-btn tv-color-btn" data-r="255" data-g="250" data-b="250" onclick="setTvColor(this, 255, 250, 250)">
                        <div class="color-swatch" style="background: rgb(255,250,250)"></div>
                    </button>
                    <button class="color-btn tv-color-btn" data-r="0" data-g="255" data-b="200" onclick="setTvColor(this, 0, 255, 200)">
                        <div class="color-swatch" style="background: rgb(0,255,200)"></div>
                    </button>
                    <!-- Colors -->
                    <button class="color-btn tv-color-btn" data-r="255" data-g="0" data-b="0" onclick="setTvColor(this, 255, 0, 0)">
                        <div class="color-swatch" style="background: rgb(255,0,0)"></div>
                    </button>
                    <button class="color-btn tv-color-btn" data-r="0" data-g="255" data-b="0" onclick="setTvColor(this, 0, 255, 0)">
                        <div class="color-swatch" style="background: rgb(0,255,0)"></div>
                    </button>
                    <button class="color-btn tv-color-btn" data-r="0" data-g="0" data-b="255" onclick="setTvColor(this, 0, 0, 255)">
                        <div class="color-swatch" style="background: rgb(0,0,255)"></div>
                    </button>
                    <button class="color-btn tv-color-btn" data-r="255" data-g="0" data-b="255" onclick="setTvColor(this, 255, 0, 255)">
                        <div class="color-swatch" style="background: rgb(255,0,255)"></div>
                    </button>
                </div>
            </div>
        </div>

        <div class="section dropdown-panel" id="tvEffectPanel">
            <div class="panel-header" onclick="toggleTvEffect()">
                <div class="section-title" style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                    <span>TV Effect</span>
                    <svg id="tvEffectChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s;">
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                </div>
            </div>
            <div class="panel-content" id="tvEffectContent">
                <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 12px;">
                    <button class="action-btn tv-effect-btn active" style="margin-top:0;" onclick="setTvEffect(this, 'solid')">Solid Color</button>
                    <button class="action-btn tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'sweep')">Center-Out Sweep</button>
                    <button class="action-btn tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'breathe')">Smooth Breathe</button>
                    <button class="action-btn tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'rainbow')">Rainbow Flow</button>
                </div>
            </div>
        </div>
"""

# I will use regex to find `<div class="toast" id="toast">`
pattern = r'(    <div class="toast" id="toast">.*)'
html = re.sub(pattern, tv_tab_html + r'\n\1', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
