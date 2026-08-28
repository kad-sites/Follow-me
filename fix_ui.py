with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Make power button slim and integrated
old_power = """        <!-- Power Button -->
        <div class="section" style="display: flex; justify-content: center; padding: 12px; margin-bottom: 8px;">
            <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 12px 24px; font-size: 16px; font-weight: bold; width: 100%; cursor: pointer; transition: all 0.2s;">
                TURN OFF
            </button>
        </div>"""

new_power = """        <div class="section" style="padding: 12px 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="section-title" style="margin-bottom: 0;">TV Power</div>
                <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 6px 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s;">
                    ON
                </button>
            </div>
        </div>"""
html = html.replace(old_power, new_power)


# 2. Add Color Temp Slider below color grid
import re
temp_slider = """
                </div>
                <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>
                <div class="section-header">
                    <div class="section-title">White Temperature</div>
                    <div class="value-display" id="tvTempVal">Warm</div>
                </div>
                <div class="slider-container">
                    <input type="range" id="tvTemp" min="0" max="100" value="0" style="touch-action: pan-y;">
                    <div class="slider-labels" style="justify-content: space-between; display: flex; font-size: 11px; color: var(--subtext); margin-top: 4px;">
                        <span>Warm</span>
                        <span>Cool</span>
                    </div>
                </div>
"""
# find the end of color grid which looks like </div>\n            </div>\n        </div>\n\n        <div class="section dropdown-panel" id="tvEffectPanel">
html = html.replace('                </div>\n            </div>\n        </div>\n\n        <div class="section dropdown-panel" id="tvEffectPanel">', temp_slider + '\n            </div>\n        </div>\n\n        <div class="section dropdown-panel" id="tvEffectPanel">')

# 3. Add new effects
new_effects = """                    <button class="tv-effect-btn" onclick="setTvEffect(this, 'rainbow')">Rainbow Flow</button>
                    <button class="tv-effect-btn" onclick="setTvEffect(this, 'chase')">Theater Chase</button>
                    <button class="tv-effect-btn" onclick="setTvEffect(this, 'twinkle')">Starry Twinkle</button>
                    <button class="tv-effect-btn" onclick="setTvEffect(this, 'fire')">Fire Effect</button>"""
html = html.replace('<button class="tv-effect-btn" onclick="setTvEffect(this, \'rainbow\')">Rainbow Flow</button>', new_effects)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
