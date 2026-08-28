import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add IDs to the tab buttons and remove hardcoded active classes
old_tabs = """        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('corridor')">Corridor (Radar)</button>
            <button class="tab-btn" onclick="switchTab('tv')">TV Backlight</button>
        </div>"""

new_tabs = """        <div class="tabs">
            <button id="btn-corridor" class="tab-btn" onclick="switchTab('corridor')">Corridor (Radar)</button>
            <button id="btn-tv" class="tab-btn" onclick="switchTab('tv')">TV Backlight</button>
        </div>
        <script>
            (function(){
                var t = localStorage.getItem('activeTab') || 'corridor';
                var btn = document.getElementById('btn-' + t);
                if(btn) btn.classList.add('active');
                
                // Also fix the dynamic header instantly so it doesn't flash
                const headerTitle = document.querySelector('.header .title');
                if (headerTitle) {
                    if (t === 'tv') {
                        headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">TV Backlight</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                    } else {
                        headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">Follow-Me</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                    }
                }
            })();
        </script>"""
html = html.replace(old_tabs, new_tabs)

# 2. Remove hardcoded display: block and active class from Corridor tab
html = html.replace('<div id="tab-corridor" class="tab-content active" style="display: block;">', '<div id="tab-corridor" class="tab-content" style="display: none;">')

# 3. Add inline script after both tabs to display the correct one instantly
old_end = '    </div> <!-- End App Container -->'
new_end = """        <script>
            (function(){
                var t = localStorage.getItem('activeTab') || 'corridor';
                var tab = document.getElementById('tab-' + t);
                if(tab) {
                    tab.style.display = 'block';
                    tab.classList.add('active');
                }
            })();
        </script>
    </div> <!-- End App Container -->"""
html = html.replace(old_end, new_end)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
