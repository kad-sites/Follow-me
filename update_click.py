import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_listener_pattern = r"document\.addEventListener\('click',\s*\([^)]*\)\s*=>\s*\{\s*const panel = document\.getElementById\('radarPanel'\);[\s\S]*?\}\);"

new_listener = '''document.addEventListener('click', (e) => {
            const panels = [
                { id: 'radarPanel', arrow: 'radarArrow', toggle: 'toggleRadar()' },
                { id: 'colorPanel', arrow: 'colorArrow', toggle: 'toggleColor()' },
                { id: 'calibPanel', arrow: 'calibArrow', toggle: 'toggleCalib()' }
            ];
            
            panels.forEach(p => {
                const panel = document.getElementById(p.id);
                const arrow = document.getElementById(p.arrow);
                if (panel && panel.style.display === 'block') {
                    const clickedInside = e.target.closest('#' + p.id) || e.target.closest('[onclick="' + p.toggle + '"]');
                    if (!clickedInside) {
                        panel.style.display = 'none';
                        arrow.innerHTML = '&#9660;';
                    }
                }
            });
        });'''

js = re.sub(old_listener_pattern, new_listener, js)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
