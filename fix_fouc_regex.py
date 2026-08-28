import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Tab buttons
tabs_pattern = r'<div class="tabs">\s*<button class="tab-btn active" onclick="switchTab\(\'corridor\'\)">Corridor \(Radar\)</button>\s*<button class="tab-btn" onclick="switchTab\(\'tv\'\)">TV Backlight</button>\s*</div>'
tabs_repl = """<div class="tabs">
            <button id="btn-corridor" class="tab-btn" onclick="switchTab('corridor')">Corridor (Radar)</button>
            <button id="btn-tv" class="tab-btn" onclick="switchTab('tv')">TV Backlight</button>
        </div>
        <script>
            (function(){
                var t = localStorage.getItem('activeTab') || 'corridor';
                var btn = document.getElementById('btn-' + t);
                if(btn) btn.classList.add('active');
                
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

html = re.sub(tabs_pattern, tabs_repl, html)

# 2. Hardcoded display block
html = re.sub(r'<div id="tab-corridor" class="tab-content active" style="display: block;">', r'<div id="tab-corridor" class="tab-content" style="display: none;">', html)

# 3. Add script at end
end_pattern = r'\s*</div>\s*<!-- End App Container -->'
end_repl = """
        <script>
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

html = re.sub(end_pattern, end_repl, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
