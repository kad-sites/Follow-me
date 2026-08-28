with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

funcs = '''        function toggleRadar() {
            const panel = document.getElementById('radarPanel');
            const arrow = document.getElementById('radarArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '?';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '?';
            }
        }

        function toggleCalib() {
            const panel = document.getElementById('calibPanel');
            const arrow = document.getElementById('calibArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '?';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '?';
            }
        }'''

# Replace the existing toggleRadar with both
import re
js = re.sub(r'        function toggleRadar\(\) \{[\s\S]*?arrow\.innerHTML = \'?\';\n            \}\n        \}', funcs, js)

js = js.replace('window.toggleRadar = toggleRadar;', 'window.toggleRadar = toggleRadar;\n        window.toggleCalib = toggleCalib;')

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
