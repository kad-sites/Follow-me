import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add CSS for tabs
tab_css = """
        .tabs {
            display: flex;
            max-width: 450px;
            width: 100%;
            background: var(--card);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
            margin-bottom: 8px;
        }
        .tab-btn {
            flex: 1;
            padding: 12px;
            background: transparent;
            color: var(--subtext);
            border: none;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .tab-btn.active {
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent);
        }
        .tab-content {
            display: none;
            width: 100%;
            max-width: 450px;
            flex-direction: column;
            gap: 12px;
        }
        .tab-content.active {
            display: flex;
        }
"""
html = html.replace('</style>', tab_css + '</style>')

# 2. Inject Tabs Nav and TV HTML
# Find the end of the header
header_end_str = 'Unable to connect to controller</div>\n    </div>'

tab_nav = """    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('corridor')">Corridor (Radar)</button>
        <button class="tab-btn" onclick="switchTab('tv')">TV Backlight</button>
    </div>

    <!-- TAB 1: CORRIDOR (Original Code) -->
    <div id="tab-corridor" class="tab-content active">"""

tv_tab_html = """
    </div>

    <!-- TAB 2: TV BACKLIGHT -->
    <div id="tab-tv" class="tab-content">
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

html = html.replace(header_end_str, header_end_str + '\n' + tab_nav)

# Find where the corridor elements end (just before the toast)
toast_str = '    <div class="toast" id="toast">Saved</div>'
html = html.replace(toast_str, tv_tab_html + '\n' + toast_str)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
