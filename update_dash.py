import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update Brightness to Follow Brightness and Base Brightness
bright_old = '''        <div class="section-header">
            <div class="section-title">Brightness</div>
            <div class="value-display" id="brightVal">100%</div>
        </div>
        <div class="slider-container">
            <input type="range" id="brightness" min="0" max="255" value="255">
        </div>'''
bright_new = '''        <div class="section-header">
            <div class="section-title">Follow Brightness</div>
            <div class="value-display" id="fBrightVal">100%</div>
        </div>
        <div class="slider-container">
            <input type="range" id="followBrightness" min="0" max="255" value="255">
        </div>
        <br>
        <div class="section-header">
            <div class="section-title">Base Brightness</div>
            <div class="value-display" id="bBrightVal">4%</div>
        </div>
        <div class="slider-container">
            <input type="range" id="baseBrightness" min="0" max="255" value="10">
        </div>'''
html = html.replace(bright_old, bright_new)

# 2. Update Follow Speed max to 50
html = html.replace('<input type="range" id="speed" min="1" max="20" value="10">', '<input type="range" id="speed" min="1" max="50" value="10">')

# 3. Add Lead Distance slider after Follow Speed
speed_sec = '''        <div class="slider-container">
            <input type="range" id="speed" min="1" max="50" value="10">
            <div class="slider-labels">
                <span>Smooth</span>
                <span>Snappy</span>
            </div>
        </div>'''
lead_sec = '''        <div class="slider-container">
            <input type="range" id="speed" min="1" max="50" value="10">
            <div class="slider-labels">
                <span>Smooth</span>
                <span>Snappy</span>
            </div>
        </div>
        <br>
        <div class="section-header">
            <div class="section-title">Lead Distance</div>
            <div class="value-display" id="leadVal">20</div>
        </div>
        <div class="slider-container">
            <input type="range" id="leadFactor" min="0" max="50" value="20">
            <div class="slider-labels">
                <span>Centered</span>
                <span>Ahead</span>
            </div>
        </div>'''
html = html.replace(speed_sec, lead_sec)

# 4. Add Color Target Toggle
color_sec_old = '''    <!-- Color Modes -->
    <div class="section">
        <div class="section-header">
            <div class="section-title">Color Mode</div>
        </div>'''
color_sec_new = '''    <!-- Color Modes -->
    <div class="section">
        <div class="section-header">
            <div class="section-title">Color Mode</div>
        </div>
        <div style="display: flex; gap: 8px; margin-bottom: 16px; background: rgba(0,0,0,0.3); padding: 4px; border-radius: 8px;">
            <button id="tgtFollowBtn" class="apply-btn active-tab" style="margin:0; font-size:12px; padding:8px; border:1px solid #60a5fa;" onclick="setColorTarget('follow')">Follow Portion</button>
            <button id="tgtBaseBtn" class="apply-btn" style="margin:0; font-size:12px; padding:8px; background:transparent; color:#94a3b8;" onclick="setColorTarget('base')">Base Strip</button>
        </div>'''
html = html.replace(color_sec_old, color_sec_new)

# 5. Fix touch-action on all sliders
html = html.replace('<input type="range"', '<input type="range" style="touch-action: pan-y;"')

with open('index.html', 'w') as f:
    f.write(html)
