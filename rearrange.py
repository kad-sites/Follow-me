import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove Fade Spread and Active Pixels from their current positions
# First, find Fade Spread block
fade_spread_pattern = r'    <div class="section">\s*<div class="section-header">\s*<div class="section-title">Fade Spread</div>[\s\S]*?</div>\s*</div>'
fade_match = re.search(fade_spread_pattern, html)
if fade_match:
    fade_html = fade_match.group(0)
    html = html.replace(fade_html, '')
else:
    print("Could not find fade spread")

# Find Active Pixels block
pixels_pattern = r'    <!-- Active Pixels -->\s*<div class="section">\s*<div class="section-header">\s*<div class="section-title"[^>]*>Active Pixels</div>[\s\S]*?</div>\s*</div>'
pixels_match = re.search(pixels_pattern, html)
if pixels_match:
    pixels_html = pixels_match.group(0)
    html = html.replace(pixels_html, '')
else:
    print("Could not find active pixels")

# 2. Insert Fade Spread inside the first section, after Glow Width
glow_pattern = r'(<div class="section-header">\s*<div class="section-title">Glow Width</div>[\s\S]*?<div class="slider-labels">\s*<span>Narrow</span>\s*<span>Wide</span>\s*</div>\s*</div>\s*</div>)'
glow_match = re.search(glow_pattern, html)
if glow_match:
    glow_html = glow_match.group(1)
    
    # Strip the outer section wrapper from fade_html
    fade_inner = re.sub(r'^\s*<div class="section">\s*', '', fade_html)
    fade_inner = re.sub(r'\s*</div>\s*$', '', fade_inner)
    
    separator = '\n        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>\n'
    
    html = html.replace(glow_html, glow_html + separator + "        " + fade_inner.strip())
else:
    print("Could not find glow width")

# 3. Create the new Active Pixels dropdown and insert after Apply button
apply_btn_pattern = r'(<!-- Apply Settings Button -->\s*<button class="apply-btn"[^>]*>Apply LED Settings</button>)'

new_pixels_html = '''
    <!-- Active Pixels -->
    <div class="section">
        <div class="section-header" style="justify-content: space-between; margin-bottom: 0; cursor: pointer; padding: 4px 0;" onclick="togglePixels()">
            <div class="section-title" style="cursor: pointer; text-decoration: underline; text-decoration-color: rgba(255,255,255,0.2); text-decoration-style: dotted;" onclick="event.stopPropagation(); promptPixelLimits()">Active Pixels</div>
            <div id="pixelsArrow" style="color: var(--subtext); font-size: 12px;">&#9660;</div>
        </div>
        <div id="pixelsPanel" style="display: none; margin-top: 16px;">
            <div style="display: flex; justify-content: flex-end; margin-bottom: 8px;">
                <div class="value-display" id="pixelsVal">150</div>
            </div>
            <div class="slider-container">
                <input type="range" style="touch-action: pan-y;" id="activePixels" min="1" max="300" value="150">
                <div class="slider-labels">
                    <span id="pixelsMinLabel">1</span>
                    <span id="pixelsMaxLabel">300</span>
                </div>
            </div>
        </div>
    </div>
'''

html = re.sub(apply_btn_pattern, r'\1\n' + new_pixels_html, html)

# Clean up empty lines
html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

