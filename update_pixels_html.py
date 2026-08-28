import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add TV Pixels slider
speed_block = """                <div class="section-header">
                    <div class="section-title">Effect Speed</div>
                    <div class="value-display" id="tvSpeedVal">50%</div>
                </div>
                <div class="slider-container">
                    <input type="range" id="tvSpeed" min="1" max="100" value="50" style="touch-action: pan-y;">
                </div>"""

new_pixels_block = """                <div class="section-header">
                    <div class="section-title">TV Pixels</div>
                    <div class="value-display" id="tvPixelsVal">27</div>
                </div>
                <div class="slider-container">
                    <input type="range" id="tvPixels" min="10" max="300" value="27" style="touch-action: pan-y;">
                </div>"""

html = html.replace(speed_block, speed_block + "\n" + new_pixels_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
