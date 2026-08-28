with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

pointer_logic = """
// Force range sliders to jump to click/tap position (fixes iOS/Android track tap bugs)
document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('pointerdown', function(e) {
        const rect = slider.getBoundingClientRect();
        let x = e.clientX - rect.left;
        if (x < 0) x = 0;
        if (x > rect.width) x = rect.width;
        
        const min = parseFloat(slider.min || 0);
        const max = parseFloat(slider.max || 100);
        const step = parseFloat(slider.step || 1);
        
        let newValue = min + (x / rect.width) * (max - min);
        
        // Snap to step
        newValue = Math.round((newValue - min) / step) * step + min;
        if (newValue > max) newValue = max;
        if (newValue < min) newValue = min;
        
        slider.value = newValue;
        slider.dispatchEvent(new Event('input'));
        slider.dispatchEvent(new Event('change'));
    });
});
"""

js += "\n" + pointer_logic

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
