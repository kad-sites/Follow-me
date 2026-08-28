import re
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

old_switch = """        function switchTab(tabId) {
            localStorage.setItem('activeTab', tabId);
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
                el.style.display = 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            const target = document.getElementById('tab-' + tabId);
            if (target) {
                target.classList.add('active');
                target.style.display = 'flex';
            }
            document.querySelectorAll('.tab-btn').forEach(btn => {
                if (btn.textContent.toLowerCase().includes(tabId === 'corridor' ? 'corridor' : 'tv')) {
                    btn.classList.add('active');
                }
            });
            activeTab = tabId;
        }"""

new_switch = """        function switchTab(tabId) {
            localStorage.setItem('activeTab', tabId);
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
                el.style.display = 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            const target = document.getElementById('tab-' + tabId);
            if (target) {
                target.classList.add('active');
                target.style.display = 'flex';
            }
            document.querySelectorAll('.tab-btn').forEach(btn => {
                if (btn.textContent.toLowerCase().includes(tabId === 'corridor' ? 'corridor' : 'tv')) {
                    btn.classList.add('active');
                }
            });
            activeTab = tabId;
            
            const headerTitle = document.querySelector('.header .title');
            if (headerTitle) {
                if (activeTab === 'tv') {
                    headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">TV Backlight</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                } else {
                    headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">Follow-Me</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                }
            }
        }"""

js = js.replace(old_switch, new_switch)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
