import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add pixelsPanel to the auto-closing listener
old_panels_array = '''const panels = [
                { id: 'radarPanel', arrow: 'radarArrow', toggle: 'toggleRadar()' },
                { id: 'colorPanel', arrow: 'colorArrow', toggle: 'toggleColor()' },
                { id: 'calibPanel', arrow: 'calibArrow', toggle: 'toggleCalib()' }
            ];'''

new_panels_array = '''const panels = [
                { id: 'radarPanel', arrow: 'radarArrow', toggle: 'toggleRadar()' },
                { id: 'colorPanel', arrow: 'colorArrow', toggle: 'toggleColor()' },
                { id: 'calibPanel', arrow: 'calibArrow', toggle: 'toggleCalib()' },
                { id: 'pixelsPanel', arrow: 'pixelsArrow', toggle: 'togglePixels()' }
            ];'''

js = js.replace(old_panels_array, new_panels_array)

# 2. Add togglePixels function
toggle_color_func = '''function toggleColor() {'''
new_toggle_pixels = '''function togglePixels() {
            const panel = document.getElementById('pixelsPanel');
            const arrow = document.getElementById('pixelsArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '&#9650;';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '&#9660;';
            }
        }
        window.togglePixels = togglePixels;
        
        function toggleColor() {'''
js = js.replace(toggle_color_func, new_toggle_pixels)

# 3. Remove applyRadarSettings and its window assignment
js = re.sub(r'function applyRadarSettings\(\) \{[\s\S]*?showToast\("Radar Command Sent to Cloud"\);\s*\}', '', js)
js = re.sub(r'window\.applyRadarSettings = applyRadarSettings;\s*', '', js)

# 4. Add Live event listeners for the dropdown sliders
# We'll put this right after the sliders.forEach(s => s.el.addEventListener('input', () => updateUI())); block
old_listeners = '''        sliders.forEach(s => {
            s.el.addEventListener('input', () => {
                updateUI();
                // throttledUpdate removed - waiting for Apply button
            });
        });'''

new_listeners = '''        sliders.forEach(s => {
            s.el.addEventListener('input', () => {
                updateUI();
            });
        });
        
        // Add live "change" listeners to all dropdown sliders so they send immediately
        const liveSliders = [
            { el: pixelsSlider, key: 'activePixels' },
            { el: densitySlider, key: 'ledDensity' },
            { el: offsetSlider, key: 'sensorOffset' },
            { el: minDistSlider, key: 'minDist' },
            { el: maxDistSlider, key: 'maxDist' },
            { el: timeoutSlider, key: 'timeout' }
        ];
        
        liveSliders.forEach(s => {
            if (s.el) {
                // Use 'change' so it fires when user lifts their finger
                s.el.addEventListener('change', () => {
                    let payload = {};
                    payload[s.key] = parseInt(s.el.value);
                    sendUpdate(payload);
                    showToast("Setting updated live");
                });
            }
        });'''
js = js.replace(old_listeners, new_listeners)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
