import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Save Tab State
tab_logic_old = """        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => {"""
tab_logic_new = """        function switchTab(tabId) {
            localStorage.setItem('activeTab', tabId);
            document.querySelectorAll('.tab-content').forEach(el => {"""
js = js.replace(tab_logic_old, tab_logic_new)

# Add init tab logic at the end of the file
js += """
        // Restore tab on load
        const savedTab = localStorage.getItem('activeTab');
        if (savedTab) {
            switchTab(savedTab);
        }
"""

# 2. Add retain to publish
js = js.replace('client.publish("kad/tvbacklit/cmd/zoheb", JSON.stringify(payload));', 'client.publish("kad/tvbacklit/cmd/zoheb", JSON.stringify(payload), { retain: true });')

# 3. Subscribe to TV topic so the web UI syncs on load
# Inside client.on('connect')
connect_old = """            if (DEVICE_MAC) {
                initCorridorConnection();
            }"""
connect_new = """            if (DEVICE_MAC) {
                initCorridorConnection();
            }
            client.subscribe("kad/tvbacklit/cmd/zoheb");"""
js = js.replace(connect_old, connect_new)

# 4. Handle incoming TV topic message to update UI
msg_old = """            try {
                const data = JSON.parse(message.toString());
                if (topic === TOPIC_STATUS) {"""
msg_new = """            try {
                const data = JSON.parse(message.toString());
                if (topic === "kad/tvbacklit/cmd/zoheb") {
                    if (data.state !== undefined) {
                        tvPower = (data.state === "ON");
                        const btn = document.getElementById('tvPowerBtn');
                        if (tvPower) {
                            btn.innerText = "ON";
                            btn.style.color = "#10b981";
                            btn.style.background = "rgba(16, 185, 129, 0.15)";
                            btn.style.borderColor = "rgba(16, 185, 129, 0.3)";
                        } else {
                            btn.innerText = "OFF";
                            btn.style.color = "#ef4444";
                            btn.style.background = "rgba(239, 68, 68, 0.15)";
                            btn.style.borderColor = "rgba(239, 68, 68, 0.3)";
                        }
                    }
                    if (data.brightness !== undefined) {
                        document.getElementById('tvBrightness').value = data.brightness;
                        document.getElementById('tvBrightVal').innerText = Math.round((data.brightness / 255) * 100) + '%';
                    }
                    if (data.speed !== undefined) {
                        tvSpeed = data.speed;
                        document.getElementById('tvSpeed').value = tvSpeed;
                        document.getElementById('tvSpeedVal').innerText = tvSpeed + '%';
                    }
                    if (data.effect !== undefined) {
                        tvEffect = data.effect;
                        document.querySelectorAll('.tv-effect-btn').forEach(el => el.classList.remove('active'));
                        // Very basic matching for UI update
                        document.querySelectorAll('.tv-effect-btn').forEach(btn => {
                            if (btn.getAttribute('onclick').includes(tvEffect)) btn.classList.add('active');
                        });
                    }
                    if (data.r !== undefined && data.g !== undefined && data.b !== undefined) {
                        tvColor = {r: data.r, g: data.g, b: data.b};
                        document.getElementById('tvColorChevron').parentElement.parentElement.style.borderLeftColor = `rgb(${data.r},${data.g},${data.b})`;
                    }
                    return;
                }
                
                if (topic === TOPIC_STATUS) {"""
js = js.replace(msg_old, msg_new)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
