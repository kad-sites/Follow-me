with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the '?' character and the missing JS
html = html.replace('<div id="calibArrow" style="color: var(--subtext); font-size: 12px;">?</div>', '<div id="calibArrow" style="color: var(--subtext); font-size: 12px;">?</div>')

# Since toggleCalib is missing, I will inject it right before function toggleRadar
if 'function toggleRadar()' in html:
    new_funcs = '''function toggleCalib() {
            const panel = document.getElementById('calibPanel');
            const arrow = document.getElementById('calibArrow');
            if(panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '?';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '?';
            }
        }
        function toggleRadar()'''
    html = html.replace('function toggleRadar()', new_funcs)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
