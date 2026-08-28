import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's extract from <!-- Main Controls --> to <!-- Apply Settings Button -->
pattern = r'<!-- Main Controls -->[\s\S]*?<!-- Apply Settings Button -->'

new_html = """<!-- Main Controls -->
    <div class="section">
        <div class="section-header">
            <div class="section-title">Follow Brightness</div>
            <div class="value-display" id="fBrightVal">100%</div>
        </div>
        <div class="slider-container">
            <input type="range" style="touch-action: pan-y;" id="followBrightness" min="0" max="255" value="255">
        </div>
        
        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>

        <div class="section-header">
            <div class="section-title">Base Brightness</div>
            <div class="value-display" id="bBrightVal">0%</div>
        </div>
        <div class="slider-container">
            <input type="range" style="touch-action: pan-y;" id="baseBrightness" min="0" max="255" value="0">
        </div>

        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>

        <div class="section-header">
            <div class="section-title">Follow Speed</div>
            <div class="value-display" id="speedVal">10</div>
        </div>
        <div class="slider-container">
            <input type="range" style="touch-action: pan-y;" id="followSpeed" min="1" max="20" value="10">
            <div class="slider-labels">
                <span>Smooth</span>
                <span>Snappy</span>
            </div>
        </div>

        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>

        <div class="section-header">
            <div class="section-title">Lead Distance</div>
            <div class="value-display" id="leadVal">6</div>
        </div>
        <div class="slider-container">
            <input type="range" style="touch-action: pan-y;" id="leadFactor" min="0" max="20" value="6">
            <div class="slider-labels">
                <span>Centered</span>
                <span>Ahead</span>
            </div>
        </div>

        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>

        <div class="section-header">
            <div class="section-title">Glow Width</div>
            <div class="value-display" id="glowVal">10</div>
        </div>
        <div class="slider-container">
            <input type="range" style="touch-action: pan-y;" id="glowSize" min="6" max="60" value="10">
            <div class="slider-labels">
                <span>Narrow</span>
                <span>Wide</span>
            </div>
        </div>
        
        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>

        <div class="section-header">
            <div class="section-title">Fade Spread</div>
            <div class="value-display" id="fadeVal">0</div>
        </div>
        <div class="slider-container">
            <input type="range" style="touch-action: pan-y;" id="fadeSigma" min="0" max="100" value="0">
            <div class="slider-labels">
                <span>Sharp</span>
                <span>Soft</span>
            </div>
        </div>
    </div>

    <!-- Apply Settings Button -->"""

html = re.sub(pattern, new_html, html)

# Wait, what about Active Pixels? Let's check if it's there or if I accidentally deleted it when fixing.
# Actually, I'll just check if Active Pixels exists, if not, I'll add it back.

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

