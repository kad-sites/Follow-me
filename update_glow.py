import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_style_code = """            // For webkit styles injection
            const style = document.createElement('style');
            style.innerHTML = `#followBrightness::-webkit-slider-runnable-track { background: linear-gradient(to right, #222, ${followColorHex}) !important; } #baseBrightness::-webkit-slider-runnable-track { background: linear-gradient(to right, #222, ${baseColorHex}) !important; }`;
            document.head.appendChild(style);"""

new_style_code = """            // Glow width calculation (center out)
            const glowMin = parseInt(glowSlider.min) || 6;
            const glowMax = parseInt(glowSlider.max) || 60;
            const glowVal = parseInt(glowSlider.value);
            const glowP = (glowVal - glowMin) / (glowMax - glowMin);
            const halfP = (glowP * 100) / 2;
            const leftEdge = 50 - halfP;
            const rightEdge = 50 + halfP;
            
            // For webkit styles injection
            let style = document.getElementById('dynamic-slider-styles');
            if (!style) {
                style = document.createElement('style');
                style.id = 'dynamic-slider-styles';
                document.head.appendChild(style);
            }
            style.innerHTML = `
                #followBrightness::-webkit-slider-runnable-track { background: linear-gradient(to right, #222, ${followColorHex}) !important; }
                #baseBrightness::-webkit-slider-runnable-track { background: linear-gradient(to right, #222, ${baseColorHex}) !important; }
                #glowSize::-webkit-slider-runnable-track { background: linear-gradient(to right, #333 0%, #333 ${leftEdge}%, ${baseColorHex} ${leftEdge}%, ${baseColorHex} ${rightEdge}%, #333 ${rightEdge}%, #333 100%) !important; }
            `;"""

js = js.replace(old_style_code, new_style_code)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
