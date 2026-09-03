with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# We need to find the entire switchTab function and replace it.
# It starts with "function switchTab(tabId) {"
# And ends before "window.switchTab = switchTab;"

match = re.search(r'function switchTab\(tabId\) \{.*?(?=window\.switchTab = switchTab;)', js, re.DOTALL)
if match:
    old_func = match.group(0)
    new_func = """function switchTab(tabId) {
            localStorage.setItem('activeTab', tabId);
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
                el.style.display = 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            const target = document.getElementById('tab-' + tabId);
            if (target) {
                target.classList.add('active');
                target.style.display = 'block'; // Or flex, doesn't matter too much
            }
            
            const btn = document.getElementById('btn-' + tabId);
            if (btn) {
                btn.classList.add('active');
            }
        }
        
        """
    js = js.replace(old_func, new_func)
    print("SUCCESS")
else:
    print("COULD NOT FIND switchTab")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
