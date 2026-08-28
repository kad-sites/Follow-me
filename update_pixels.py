import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_pixels_html = '''                <div class="section-header">
                    <div class="section-title">Active Pixels</div>
                    <div class="value-display" id="pixelsVal">150</div>
                </div>
                <div class="slider-container">
                    <input type="range" style="touch-action: pan-y;" id="activePixels" min="10" max="300" value="150">
                    <div class="slider-labels">
                        <span>10</span>
                        <span>300</span>
                    </div>
                </div>'''

new_pixels_html = '''                <div class="section-header">
                    <div class="section-title" style="cursor: pointer; text-decoration: underline; text-decoration-color: rgba(255,255,255,0.2); text-decoration-style: dotted;" onclick="promptPixelLimits()">Active Pixels</div>
                    <div class="value-display" id="pixelsVal">150</div>
                </div>
                <div class="slider-container">
                    <input type="range" style="touch-action: pan-y;" id="activePixels" min="1" max="300" value="150">
                    <div class="slider-labels">
                        <span id="pixelsMinLabel">1</span>
                        <span id="pixelsMaxLabel">300</span>
                    </div>
                </div>'''

if old_pixels_html in html:
    html = html.replace(old_pixels_html, new_pixels_html)
else:
    print("Could not find old_pixels_html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
