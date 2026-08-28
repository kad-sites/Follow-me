import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

color_injection = """        function toggleTvColor() {
            const content = document.getElementById('tvColorContent');
            const chevron = document.getElementById('tvColorChevron');
            content.classList.toggle('open');
            chevron.style.transform = content.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
            
            // Auto close Effect panel
            if (content.classList.contains('open')) {
                const effContent = document.getElementById('tvEffectContent');
                const effChevron = document.getElementById('tvEffectChevron');
                if (effContent) {
                    effContent.classList.remove('open');
                    effChevron.style.transform = 'rotate(0deg)';
                }
            }
        }"""

effect_injection = """        function toggleTvEffect() {
            const content = document.getElementById('tvEffectContent');
            const chevron = document.getElementById('tvEffectChevron');
            content.classList.toggle('open');
            chevron.style.transform = content.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
            
            // Auto close Color panel
            if (content.classList.contains('open')) {
                const colContent = document.getElementById('tvColorContent');
                const colChevron = document.getElementById('tvColorChevron');
                if (colContent) {
                    colContent.classList.remove('open');
                    colChevron.style.transform = 'rotate(0deg)';
                }
            }
        }"""

js = re.sub(r'function toggleTvColor\(\).*?rotate\(0deg\)\';\s*\}', color_injection, js, flags=re.DOTALL)
js = re.sub(r'function toggleTvEffect\(\).*?rotate\(0deg\)\';\s*\}', effect_injection, js, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
