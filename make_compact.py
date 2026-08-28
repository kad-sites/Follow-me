import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make CSS more compact (15% reduction in sizes/paddings)
html = html.replace('.section {\n            background: var(--surface);', '.section {\n            background: var(--surface);\n            margin-bottom: 12px;')
html = html.replace('padding: 20px;\n            border-radius: 16px;', 'padding: 16px;\n            border-radius: 12px;')

html = html.replace('.section-header {\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            margin-bottom: 12px;', '.section-header {\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            margin-bottom: 8px;')

html = html.replace('height: 8px;', 'height: 6px;')
html = html.replace('width: 24px;\n            height: 24px;', 'width: 20px;\n            height: 20px;')
html = html.replace('margin-top: -8px;', 'margin-top: -7px;') # Thumb offset

html = html.replace('.tv-effect-btn {\n            background: rgba(255, 255, 255, 0.03);\n            border: 1px solid rgba(255, 255, 255, 0.05);\n            color: var(--text);\n            padding: 12px 16px;\n            border-radius: 8px;\n            font-size: 14px;', 
'.tv-effect-btn {\n            background: rgba(255, 255, 255, 0.03);\n            border: 1px solid rgba(255, 255, 255, 0.05);\n            color: var(--text);\n            padding: 10px 14px;\n            border-radius: 6px;\n            font-size: 13px;')

html = html.replace('.color-swatch {\n            width: 32px;\n            height: 32px;', '.color-swatch {\n            width: 28px;\n            height: 28px;')

# Dynamic Title Header
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

switch_tab_old = """        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
                el.style.display = 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).style.display = 'block';
            setTimeout(() => {
                document.getElementById(tabId).classList.add('active');
            }, 10);
            event.target.classList.add('active');
            activeTab = tabId.replace('tab-', '');"""

switch_tab_new = """        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
                el.style.display = 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).style.display = 'block';
            setTimeout(() => {
                document.getElementById(tabId).classList.add('active');
            }, 10);
            event.target.classList.add('active');
            activeTab = tabId.replace('tab-', '');
            
            const headerTitle = document.querySelector('.header h1');
            if (activeTab === 'tv') {
                headerTitle.innerHTML = 'TV Backlit <span style="font-weight: 300; opacity: 0.7;">Controller</span>';
            } else {
                headerTitle.innerHTML = 'Follow-Me <span style="font-weight: 300; opacity: 0.7;">Controller</span>';
            }"""

js = js.replace(switch_tab_old, switch_tab_new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
