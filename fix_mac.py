import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add MAC Address overlay to Corridor tab
mac_overlay = """
    <div id="mac-overlay" style="display: none; position: absolute; inset: 0; background: var(--bg); z-index: 100; flex-direction: column; align-items: center; justify-content: center; padding: 24px;">
        <h2 style="margin-bottom: 16px; text-align: center;">Corridor Setup</h2>
        <p style="margin-bottom: 24px; color: var(--subtext); text-align: center;">Enter your ESP32 MAC Address to connect.</p>
        <input type="text" id="macInput" placeholder="3C8A1F0961D4" style="padding: 12px; border-radius: 8px; border: 1px solid var(--border); background: var(--card); color: white; width: 100%; max-width: 300px; margin-bottom: 16px; font-size: 16px;">
        <button onclick="saveMac()" style="padding: 12px 24px; background: var(--accent); color: #000; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; max-width: 300px; font-size: 16px;">Connect</button>
    </div>
"""

# Insert mac overlay inside tab-corridor
html = html.replace('<div id="tab-corridor" class="tab-content active">', '<div id="tab-corridor" class="tab-content active" style="position: relative;">\n' + mac_overlay)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)


with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Replace the prompt logic
prompt_logic_old = """
        let storedMac = localStorage.getItem('DEVICE_MAC');
        if (!storedMac) {
            storedMac = prompt("Enter Device ID (MAC Address):", "3C8A1F0961D4") || "3C8A1F0961D4";
            localStorage.setItem('DEVICE_MAC', storedMac);
        }
        const DEVICE_MAC = storedMac;
        const TOPIC_STATUS = `followme/${DEVICE_MAC}/status`;
        const TOPIC_RADAR = `followme/${DEVICE_MAC}/radar`;
        const TOPIC_CMD = `followme/${DEVICE_MAC}/cmd`;
        
        const client = mqtt.connect('wss://broker.hivemq.com:8884/mqtt');

        client.on('connect', () => {
            console.log('Connected to HiveMQ Cloud');
            client.subscribe(TOPIC_STATUS);
            client.subscribe(TOPIC_RADAR);
            if(statusDot) statusDot.classList.add('connected');
            document.getElementById('connErrorMsg').style.display = 'none';
            isConnected = true;
            showToast("Cloud Connected");
            sendUpdate({ request: "status" });
        });
"""

prompt_logic_new = """
        let DEVICE_MAC = localStorage.getItem('DEVICE_MAC');
        let TOPIC_STATUS, TOPIC_RADAR, TOPIC_CMD;
        
        const client = mqtt.connect('wss://broker.hivemq.com:8884/mqtt');

        function initCorridorConnection() {
            if (!DEVICE_MAC) {
                document.getElementById('mac-overlay').style.display = 'flex';
                return;
            }
            document.getElementById('mac-overlay').style.display = 'none';
            
            TOPIC_STATUS = `followme/${DEVICE_MAC}/status`;
            TOPIC_RADAR = `followme/${DEVICE_MAC}/radar`;
            TOPIC_CMD = `followme/${DEVICE_MAC}/cmd`;
            
            if (client.connected) {
                client.subscribe(TOPIC_STATUS);
                client.subscribe(TOPIC_RADAR);
                sendUpdate({ request: "status" });
            }
        }

        window.saveMac = function() {
            const val = document.getElementById('macInput').value.trim();
            if(val) {
                DEVICE_MAC = val;
                localStorage.setItem('DEVICE_MAC', DEVICE_MAC);
                initCorridorConnection();
            }
        };

        client.on('connect', () => {
            console.log('Connected to HiveMQ Cloud');
            if (DEVICE_MAC) {
                initCorridorConnection();
            }
            if(statusDot) statusDot.classList.add('connected');
            document.getElementById('connErrorMsg').style.display = 'none';
            isConnected = true;
            showToast("Cloud Connected");
        });

        // call init on load to show overlay if needed
        initCorridorConnection();
"""

js = js.replace(prompt_logic_old, prompt_logic_new)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
