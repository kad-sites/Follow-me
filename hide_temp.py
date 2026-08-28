with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_block = """            <div class="section-header">
                <div class="section-title">White Temperature</div>
                    <div class="value-display" id="tvTempVal">Warm</div>
                </div>
                <div class="slider-container">
                    <input type="range" id="tvTemp" min="0" max="100" value="0" style="touch-action: pan-y;">
                    <div class="slider-labels" style="justify-content: space-between; display: flex; font-size: 11px; color: var(--subtext); margin-top: 4px;">
                        <span>Warm</span>
                        <span>Cool</span>
                    </div>
                </div>"""
new_block = """            <div id="tvTempBlock">
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
            </div>"""

html = html.replace(old_block, new_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
