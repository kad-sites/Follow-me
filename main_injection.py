import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add TV global state
tv_state = """
        let activeTab = 'corridor';
        let tvColor = { r: 255, g: 147, b: 41 };
        let tvEffect = 'solid';
        
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById('tab-' + tabId).classList.add('active');
            event.currentTarget.classList.add('active');
            activeTab = tabId;
        }

        function toggleTvColor() {
            const content = document.getElementById('tvColorContent');
            const chevron = document.getElementById('tvColorChevron');
            content.classList.toggle('open');
            chevron.style.transform = content.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
        }

        function toggleTvEffect() {
            const content = document.getElementById('tvEffectContent');
            const chevron = document.getElementById('tvEffectChevron');
            content.classList.toggle('open');
            chevron.style.transform = content.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
        }

        function setTvColor(btn, r, g, b) {
            document.querySelectorAll('.tv-color-btn').forEach(el => el.classList.remove('active'));
            if(btn) btn.classList.add('active');
            tvColor = { r, g, b };
            sendTvUpdate();
        }

        function setTvEffect(btn, effect) {
            document.querySelectorAll('.tv-effect-btn').forEach(el => el.classList.remove('active'));
            if(btn) btn.classList.add('active');
            tvEffect = effect;
            sendTvUpdate();
        }

        function sendTvUpdate() {
            if (!isConnected) return;
            const b = parseInt(document.getElementById('tvBrightness').value);
            const payload = {
                effect: tvEffect,
                brightness: b,
                r: tvColor.r,
                g: tvColor.g,
                b: tvColor.b
            };
            const msg = new Paho.Message(JSON.stringify(payload));
            msg.destinationName = "kad/tvbacklit/cmd";
            client.send(msg);
            showToast("TV Sent");
        }
"""

js = js.replace('let isConnected = false;', 'let isConnected = false;\n' + tv_state)

# Add listener for TV brightness
slider_listeners = """
        document.getElementById('tvBrightness').addEventListener('input', (e) => {
            const v = e.target.value;
            const pct = Math.round((v / 255) * 100);
            document.getElementById('tvBrightVal').innerText = pct + '%';
            
            // gradient logic
            const min = e.target.min || 0;
            const max = e.target.max || 100;
            const val = e.target.value;
            const percentage = ((val - min) / (max - min)) * 100;
            e.target.style.background = `linear-gradient(to right, rgb(${tvColor.r}, ${tvColor.g}, ${tvColor.b}) ${percentage}%, #333 ${percentage}%)`;
        });

        document.getElementById('tvBrightness').addEventListener('change', () => {
            sendTvUpdate();
        });
"""
js = js.replace("updateUI();", "updateUI();\n" + slider_listeners)

# Also close TV dropdowns when clicking outside
click_listener = """
            if (activeTab === 'tv') {
                const tvColorPanel = document.getElementById('tvColorPanel');
                if (!tvColorPanel.contains(e.target)) {
                    document.getElementById('tvColorContent').classList.remove('open');
                    document.getElementById('tvColorChevron').style.transform = 'rotate(0deg)';
                }
                const tvEffectPanel = document.getElementById('tvEffectPanel');
                if (!tvEffectPanel.contains(e.target)) {
                    document.getElementById('tvEffectContent').classList.remove('open');
                    document.getElementById('tvEffectChevron').style.transform = 'rotate(0deg)';
                }
            }
"""
js = js.replace('if (!activePixelsPanel.contains(e.target)) {', click_listener + '\n            if (!activePixelsPanel.contains(e.target)) {')

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
