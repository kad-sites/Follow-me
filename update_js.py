with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# 1. State variables
js = js.replace("let tvEffect = 'solid';", "let tvEffect = 'solid';\n        let tvPower = true;\n        let tvSpeed = 50;")

# 2. sendTvUpdate payload
send_update_old = """            const payload = {
                effect: tvEffect,
                brightness: b,
                r: tvColor.r,
                g: tvColor.g,
                b: tvColor.b
            };"""
send_update_new = """            const payload = {
                state: tvPower ? "ON" : "OFF",
                effect: tvEffect,
                speed: tvSpeed,
                brightness: b,
                r: tvColor.r,
                g: tvColor.g,
                b: tvColor.b
            };"""
js = js.replace(send_update_old, send_update_new)

# 3. TV toggle power function
power_func = """
        function toggleTvPower() {
            tvPower = !tvPower;
            const btn = document.getElementById('tvPowerBtn');
            if (tvPower) {
                btn.innerText = "TURN OFF";
                btn.style.color = "#10b981";
                btn.style.background = "rgba(16, 185, 129, 0.15)";
                btn.style.borderColor = "rgba(16, 185, 129, 0.3)";
            } else {
                btn.innerText = "TURN ON";
                btn.style.color = "#ef4444";
                btn.style.background = "rgba(239, 68, 68, 0.15)";
                btn.style.borderColor = "rgba(239, 68, 68, 0.3)";
            }
            sendTvUpdate();
        }
"""
js = js.replace("function switchTab(tabId) {", power_func + "\n        function switchTab(tabId) {")

# 4. Remove orange gradient from tvBrightness
old_bright_listener = r"        const tvBrightEl = document.getElementById\('tvBrightness'\);\s*if \(tvBrightEl\) \{.*?\n        \}"
new_bright_listener = """
        const tvBrightEl = document.getElementById('tvBrightness');
        if (tvBrightEl) {
            tvBrightEl.addEventListener('input', (e) => {
                const pct = Math.round((e.target.value / 255) * 100);
                document.getElementById('tvBrightVal').innerText = pct + '%';
            });
            tvBrightEl.addEventListener('change', () => {
                sendTvUpdate();
            });
        }

        const tvSpeedEl = document.getElementById('tvSpeed');
        if (tvSpeedEl) {
            tvSpeedEl.addEventListener('input', (e) => {
                document.getElementById('tvSpeedVal').innerText = e.target.value + '%';
            });
            tvSpeedEl.addEventListener('change', (e) => {
                tvSpeed = parseInt(e.target.value);
                sendTvUpdate();
            });
        }

        const tvTempEl = document.getElementById('tvTemp');
        if (tvTempEl) {
            tvTempEl.addEventListener('input', (e) => {
                const val = parseInt(e.target.value); // 0 to 100
                document.getElementById('tvTempVal').innerText = val < 30 ? "Warm" : (val > 70 ? "Cool" : "Neutral");
                // Lerp between Warm (255, 147, 41) and Cool (255, 255, 255)
                const r = 255;
                const g = Math.round(147 + ((255 - 147) * (val / 100.0)));
                const b = Math.round(41 + ((255 - 41) * (val / 100.0)));
                tvColor = {r, g, b};
                
                // Remove active class from color grid
                document.querySelectorAll('.tv-color-btn').forEach(btn => btn.classList.remove('active'));
            });
            tvTempEl.addEventListener('change', () => {
                sendTvUpdate();
            });
        }
"""
js = re.sub(old_bright_listener, new_bright_listener, js, flags=re.DOTALL)

# 5. Add toggleTvPower to window exports
js = js.replace("window.sendTvUpdate = sendTvUpdate;", "window.sendTvUpdate = sendTvUpdate;\n        window.toggleTvPower = toggleTvPower;")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
