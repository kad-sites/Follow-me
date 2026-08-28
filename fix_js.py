import re
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

pattern = r"(activeTab = tabId\.replace\('tab-', ''\);)"
replacement = r"""\1
            
            const headerTitle = document.querySelector('.header h1');
            if (activeTab === 'tv') {
                headerTitle.innerHTML = 'TV Backlit <span style="font-weight: 300; opacity: 0.7;">Controller</span>';
            } else {
                headerTitle.innerHTML = 'Follow-Me <span style="font-weight: 300; opacity: 0.7;">Controller</span>';
            }"""

js = re.sub(pattern, replacement, js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
