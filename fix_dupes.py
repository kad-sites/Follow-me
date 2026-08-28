import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# The block to remove:
#         document.getElementById('tvBrightness').addEventListener('input', (e) => {
#             const v = e.target.value;
#             const pct = Math.round((v / 255) * 100);
#             document.getElementById('tvBrightVal').innerText = pct + '%';
#             
#             // gradient logic
#             const min = e.target.min || 0;
#             const max = e.target.max || 100;
#             const val = e.target.value;
#             const percentage = ((val - min) / (max - min)) * 100;
#             e.target.style.background = `linear-gradient(to right, rgb(${tvColor.r}, ${tvColor.g}, ${tvColor.b}) ${percentage}%, #333 ${percentage}%)`;
#         });
# 
#         document.getElementById('tvBrightness').addEventListener('change', () => {
#             sendTvUpdate();
#         });

pattern = r"        document\.getElementById\('tvBrightness'\)\.addEventListener\('input', \(e\) => \{[\s\S]*?sendTvUpdate\(\);\s*\}\);"

js = re.sub(pattern, "", js)

# Also fix the missing updateUI in sliders.forEach:
#         sliders.forEach(s => {
#             s.el.addEventListener('input', () => {
#                 updateUI();
# 
#             });
#         });

pattern_sliders = r"(sliders\.forEach\(s => \{\s*s\.el\.addEventListener\('input', \(\) => \{\s*updateUI\(\);\s*)\}\);\s*\}\);"
replacement_sliders = r"\1throttledUpdate({ [s.key]: parseInt(s.el.value) });\n            });\n        });"

js = re.sub(pattern_sliders, replacement_sliders, js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
