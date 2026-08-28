import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

color_injection = """
                // Auto-close effect panel
                const effContent = document.getElementById('tvEffectContent');
                const effChev = document.getElementById('tvEffectChevron');
                if (effContent && effContent.style.maxHeight) {
                    effContent.style.maxHeight = null;
                    effChev.style.transform = 'rotate(0deg)';
                }
"""

effect_injection = """
                // Auto-close color panel
                const colContent = document.getElementById('tvColorContent');
                const colChev = document.getElementById('tvColorChevron');
                if (colContent && colContent.style.maxHeight) {
                    colContent.style.maxHeight = null;
                    colChev.style.transform = 'rotate(0deg)';
                }
"""

# inject inside toggleTvColor after rotate(180deg)
js = re.sub(r'(function toggleTvColor\(\).*?chev\.style\.transform = \'rotate\(180deg\)\';)', r'\1' + color_injection, js, flags=re.DOTALL)

# inject inside toggleTvEffect
js = re.sub(r'(function toggleTvEffect\(\).*?chev\.style\.transform = \'rotate\(180deg\)\';)', r'\1' + effect_injection, js, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
