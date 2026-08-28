import re
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add TV Pixels slider after Effect Speed slider container
speed_pattern = r'(<div class="section-title">Effect Speed</div>.*?<input type="range" id="tvSpeed"[^>]*>.*?</div>)'
pixels_html = """
                <div class="section-header" style="margin-top: 8px;">
                    <div class="section-title">TV Pixels</div>
                    <div class="value-display" id="tvPixelsVal">27</div>
                </div>
                <div class="slider-container">
                    <input type="range" id="tvPixels" min="10" max="300" value="27" style="touch-action: pan-y;">
                </div>"""

html = re.sub(speed_pattern, r'\1' + pixels_html, html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add tvPixels listener
listeners_pattern = r"(const speedSlider = document\.getElementById\('followSpeed'\);)"
listeners_repl = r"""\1
        document.getElementById('tvSpeed').addEventListener('input', (e) => {
            tvSpeed = parseInt(e.target.value);
            document.getElementById('tvSpeedVal').innerText = tvSpeed + '%';
            throttledTvUpdate();
        });
        document.getElementById('tvPixels').addEventListener('input', (e) => {
            tvPixels = parseInt(e.target.value);
            document.getElementById('tvPixelsVal').innerText = tvPixels;
            throttledTvUpdate();
        });
"""
# Wait, I didn't see where the tvSpeed event listener was originally. Let me just inject it before `function toggleTvPower()`
inject_pattern = r"(function toggleTvPower\(\) \{)"
inject_repl = r"""
        document.getElementById('tvSpeed').addEventListener('input', (e) => {
            tvSpeed = parseInt(e.target.value);
            document.getElementById('tvSpeedVal').innerText = tvSpeed + '%';
            if (isConnected) throttledTvUpdate();
        });
        document.getElementById('tvPixels').addEventListener('input', (e) => {
            tvPixels = parseInt(e.target.value);
            document.getElementById('tvPixelsVal').innerText = tvPixels;
            if (isConnected) throttledTvUpdate();
        });
        
        let tvTimeoutId;
        function throttledTvUpdate() {
            clearTimeout(tvTimeoutId);
            tvTimeoutId = setTimeout(sendTvUpdate, 100);
        }
        
\1"""
js = re.sub(inject_pattern, inject_repl, js)

# Add to sync logic
sync_pattern = r"(document\.getElementById\('tvTemp'\)\.value = tvTemp;\s*\})"
sync_repl = r"""\1
                  if (data.pixels !== undefined) {
                      tvPixels = data.pixels;
                      document.getElementById('tvPixels').value = tvPixels;
                      document.getElementById('tvPixelsVal').innerText = tvPixels;
                  }"""
js = re.sub(sync_pattern, sync_repl, js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
