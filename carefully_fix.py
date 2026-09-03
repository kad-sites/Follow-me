with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
old_block = r"""        function switchTab\(tabId\) \{
            localStorage\.setItem\('activeTab', tabId\);
            document\.querySelectorAll\('\.tab-content'\)\.forEach\(el => \{
                el\.classList\.remove\('active'\);
                el\.style\.display = 'none';
            \}\);
            document\.querySelectorAll\('\.tab-btn'\)\.forEach\(el => el\.classList\.remove\('active'\)\);
            
            const target = document\.getElementById\('tab-' \+ tabId\);
            if \(target\) \{
                target\.classList\.add\('active'\);
                target\.style\.display = 'flex';
            \}
            document\.querySelectorAll\('\.tab-btn'\)\.forEach\(btn => \{
                if \(btn\.textContent\.toLowerCase\(\)\.includes\(tabId === 'corridor' \? 'corridor' : 'tv'\)\) \{
                    btn\.classList\.add\('active'\);
                \}
            \}\);
            activeTab = tabId;
            \n\n        \}"""

new_block = """        function switchTab(tabId) {
            localStorage.setItem('activeTab', tabId);
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
                el.style.display = 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            const target = document.getElementById('tab-' + tabId);
            if (target) {
                target.classList.add('active');
                target.style.display = 'block';
            }
            
            const btn = document.getElementById('btn-' + tabId);
            if (btn) {
                btn.classList.add('active');
            }
            activeTab = tabId;
        }"""

js = re.sub(old_block, new_block, js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

