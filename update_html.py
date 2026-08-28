with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add Power Button, Speed Slider, and fix Brightness slider
power_and_sliders = """
        <!-- Power Button -->
        <div class="section" style="display: flex; justify-content: center; padding: 12px;">
            <button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 12px 24px; font-size: 16px; font-weight: bold; width: 100%; cursor: pointer; transition: all 0.2s;">
                ? TURN OFF
            </button>
        </div>

        <div class="section">
            <div class="section-header">
                <div class="section-title">TV Brightness</div>
                <div class="value-display" id="tvBrightVal">12%</div>
            </div>
            <div class="slider-container">
                <input type="range" style="touch-action: pan-y;" id="tvBrightness" min="0" max="255" value="30">
            </div>

            <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>

            <div class="section-header">
                <div class="section-title">Effect Speed</div>
                <div class="value-display" id="tvSpeedVal">50%</div>
            </div>
            <div class="slider-container">
                <input type="range" style="touch-action: pan-y;" id="tvSpeed" min="1" max="100" value="50">
            </div>
        </div>
"""

import re
html = re.sub(r'<div class="section">\s*<div class="section-header">\s*<div class="section-title">TV Brightness.*?</div>', power_and_sliders, html, flags=re.DOTALL)


# 2. Add Color Temp Slider below the Color Grid
temp_slider = """
                <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>
                <div class="section-header">
                    <div class="section-title">White Temperature</div>
                    <div class="value-display" id="tvTempVal">Warm</div>
                </div>
                <div class="slider-container">
                    <input type="range" style="touch-action: pan-y;" id="tvTemp" min="0" max="100" value="0">
                    <div class="slider-labels" style="justify-content: space-between; display: flex; font-size: 11px; color: var(--subtext); margin-top: 4px;">
                        <span>Warm</span>
                        <span>Cool</span>
                    </div>
                </div>
"""
html = html.replace('<!-- End Color Grid -->', '<!-- End Color Grid -->' + temp_slider)

# 3. Add new effects
new_effects = """
                    <button class="tv-effect-btn" onclick="setTvEffect(this, 'chase')">Theater Chase</button>
                    <button class="tv-effect-btn" onclick="setTvEffect(this, 'twinkle')">Starry Twinkle</button>
                    <button class="tv-effect-btn" onclick="setTvEffect(this, 'fire')">Fire Effect</button>
"""
html = html.replace('<button class="tv-effect-btn" onclick="setTvEffect(this, \'rainbow\')">Rainbow Flow</button>', '<button class="tv-effect-btn" onclick="setTvEffect(this, \'rainbow\')">Rainbow Flow</button>\n' + new_effects)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
