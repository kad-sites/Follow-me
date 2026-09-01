import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add tab button
old_tabs = """<button id="btn-corridor" class="tab-btn" onclick="switchTab('corridor')">Corridor (Radar)</button>
          <button id="btn-tv" class="tab-btn" onclick="switchTab('tv')">TV Backlight</button>"""
new_tabs = """<button id="btn-corridor" class="tab-btn" onclick="switchTab('corridor')">Radar</button>
          <button id="btn-tv" class="tab-btn" onclick="switchTab('tv')">TV</button>
          <button id="btn-pixora" class="tab-btn active" onclick="switchTab('pixora')">Pixora</button>"""
html = html.replace(old_tabs, new_tabs)

# Make Pixora default active for development, remove active from others
html = html.replace('class="tab-btn active" onclick="switchTab(\'corridor\')"', 'class="tab-btn" onclick="switchTab(\'corridor\')"')
html = html.replace('class="tab-btn active" onclick="switchTab(\'tv\')"', 'class="tab-btn" onclick="switchTab(\'tv\')"')


# 2. Add tab content at the end before closing tags
pixora_html = """
        <!-- PIXORA TAB -->
        <div id="tab-pixora" class="tab-content" style="display: block;">
          <div class="section">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <span style="font-size: 14px; font-weight: 500;">Power</span>
                  <label class="switch">
                      <input type="checkbox" id="pxPower" onchange="togglePxPower()" checked>
                      <span class="slider round"></span>
                  </label>
              </div>
          </div>

          <div class="section">
              <div class="section-header">
                  <div class="section-title">Brightness</div>
                  <div class="value-display" id="pxBrightVal">24%</div>
              </div>
              <div class="slider-container">
                  <input type="range" id="pxBrightness" min="0" max="255" value="60" style="touch-action: pan-y;">
              </div>
              <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 4px 0;"></div>
              <div class="section-header">
                  <div class="section-title">Effect Speed</div>
                  <div class="value-display" id="pxSpeedVal">50%</div>
              </div>
              <div class="slider-container">
                  <input type="range" id="pxSpeed" min="1" max="100" value="50" style="touch-action: pan-y;">
              </div>
          </div>

          <div class="section dropdown-panel" id="pxColorPanel">
              <div class="panel-header" onclick="togglePxColor()">
                  <div class="section-title" style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                      <span>Matrix Color</span>
                      <svg id="pxColorChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s; transform: rotate(0deg);">
                          <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                  </div>
              </div>
              <div class="panel-content" id="pxColorContent">
                  <div class="color-grid" style="margin-top: 12px;">
                      <!-- Warm/Whites -->
                      <button class="color-btn px-color-btn active" data-r="255" data-g="147" data-b="41" onclick="setPxColor(this, 255, 147, 41)">
                          <div class="color-swatch" style="background: rgb(255,147,41)"></div>
                      </button>
                      <button class="color-btn px-color-btn" data-r="255" data-g="214" data-b="170" onclick="setPxColor(this, 255, 214, 170)">
                          <div class="color-swatch" style="background: rgb(255,214,170)"></div>
                      </button>
                      <button class="color-btn px-color-btn" data-r="255" data-g="250" data-b="250" onclick="setPxColor(this, 255, 250, 250)">
                          <div class="color-swatch" style="background: rgb(255,250,250)"></div>
                      </button>
                      <!-- Base Colors -->
                      <button class="color-btn px-color-btn" data-r="0" data-g="255" data-b="200" onclick="setPxColor(this, 0, 255, 200)">
                          <div class="color-swatch" style="background: rgb(0,255,200)"></div>
                      </button>
                      <button class="color-btn px-color-btn" data-r="255" data-g="0" data-b="0" onclick="setPxColor(this, 255, 0, 0)">
                          <div class="color-swatch" style="background: rgb(255,0,0)"></div>
                      </button>
                      <button class="color-btn px-color-btn" data-r="0" data-g="255" data-b="0" onclick="setPxColor(this, 0, 255, 0)">
                          <div class="color-swatch" style="background: rgb(0,255,0)"></div>
                      </button>
                      <button class="color-btn px-color-btn" data-r="0" data-g="0" data-b="255" onclick="setPxColor(this, 0, 0, 255)">
                          <div class="color-swatch" style="background: rgb(0,0,255)"></div>
                      </button>
                      <button class="color-btn px-color-btn" data-r="255" data-g="0" data-b="255" onclick="setPxColor(this, 255, 0, 255)">
                          <div class="color-swatch" style="background: rgb(255,0,255)"></div>
                      </button>
                      <button class="color-btn px-color-btn" data-r="255" data-g="255" data-b="0" onclick="setPxColor(this, 255, 255, 0)">
                          <div class="color-swatch" style="background: rgb(255,255,0)"></div>
                      </button>
                      <button class="color-btn px-color-btn" style="background: linear-gradient(45deg, red, orange, yellow, green, blue, purple);" onclick="setPxRandomColor()">
                          <div class="color-swatch" style="background: transparent; border: 2px solid white;"></div>
                      </button>
                  </div>
              </div>
          </div>

          <div class="section dropdown-panel" id="pxEffectPanel">
              <div class="panel-header" onclick="togglePxEffect()">
                  <div class="section-title" style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                      <span>Matrix Effect</span>
                      <svg id="pxEffectChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s;">
                          <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                  </div>
              </div>
              <div class="panel-content" id="pxEffectContent">
                  <div style="display: flex; flex-direction: column; gap: 2px; margin-top: 4px;">
                      <button class="effect-btn px-effect-btn active" onclick="setPxEffect(this, 'solid')">Solid Color</button>
                      <button class="effect-btn px-effect-btn" onclick="setPxEffect(this, 'tetris')">Tetris Animation</button>
                      <button class="effect-btn px-effect-btn" onclick="setPxEffect(this, 'matrix_rain')">Matrix Rain</button>
                      <button class="effect-btn px-effect-btn" onclick="setPxEffect(this, 'plasma')">Plasma Waves</button>
                      <button class="effect-btn px-effect-btn" onclick="setPxEffect(this, 'game_of_life')">Game of Life</button>
                      <button class="effect-btn px-effect-btn" onclick="setPxEffect(this, 'fire')">2D Fire</button>
                  </div>
              </div>
          </div>

          <div id="savePxBtnContainer" style="margin-top: 8px; margin-bottom: 24px;">
              <button onclick="savePxSettings()" style="width: 100%; background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 12px; font-size: 14px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
                  Save Settings to Device
              </button>
          </div>
        </div>
"""

# Hide the TV tab by default
html = html.replace('id="tab-tv" class="tab-content" style="display: block;"', 'id="tab-tv" class="tab-content" style="display: none;"')
html = html.replace('id="tab-corridor" class="tab-content" style="display: block;"', 'id="tab-corridor" class="tab-content" style="display: none;"')

# Inject before the final closing divs
html = html.replace('</div> <!-- End tab-tv -->', '</div> <!-- End tab-tv -->\n' + pixora_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
