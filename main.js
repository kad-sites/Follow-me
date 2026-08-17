import mqtt from 'mqtt';

// Color Presets Definition
        const colorPresets = [
            { group: "Whites", name: "Warm White", r: 255, g: 147, b: 41, ui: "#ff9329" },
            { group: "Whites", name: "Natural White", r: 255, g: 214, b: 170, ui: "#ffd6aa" },
            { group: "Whites", name: "Cool White", r: 255, g: 250, b: 250, ui: "#fffafa" },
            { group: "Accent", name: "Aqua", r: 0, g: 255, b: 200, ui: "#00ffc8" },
            { group: "Pastels", name: "Pastel Pink", r: 255, g: 182, b: 193, ui: "#ffb6c1" },
            { group: "Pastels", name: "Pastel Lavender", r: 200, g: 162, b: 255, ui: "#c8a2ff" },
            { group: "Pastels", name: "Pastel Mint", r: 152, g: 255, b: 200, ui: "#98ffc8" },
            { group: "Pastels", name: "Pastel Peach", r: 255, g: 218, b: 185, ui: "#ffdab9" },
            { group: "Pastels", name: "Pastel Sky", r: 135, g: 206, b: 250, ui: "#87cefa" }
        ];

        // State
        let currentColorHex = "#ff9329";
        let isConnected = false;
        
        // DOM Elements
        const statusDot = document.getElementById('statusDot');
        const brightSlider = document.getElementById('brightness');
        const speedSlider = document.getElementById('speed');
        const glowSlider = document.getElementById('glowSize');
        const fadeSlider = document.getElementById('fadeSigma');
        const colorGrid = document.getElementById('colorGrid');
        const toast = document.getElementById('toast');

        // Render Color Buttons
        function renderColors() {
            let html = '';
            
            colorPresets.forEach(c => {
                html += `
                    <button class="color-btn" data-name="${c.name}" onclick="selectColor('${c.name}', ${c.r}, ${c.g}, ${c.b}, '${c.ui}')">
                        <div class="color-swatch" style="background-color: ${c.ui}; box-shadow: 0 4px 10px ${c.ui}44;"></div>
                        <div class="color-name">${c.name}</div>
                    </button>
                `;
            });
            colorGrid.innerHTML = html;
        }
        renderColors();

        // Update UI Visuals
        function updateUI() {
            document.getElementById('brightVal').innerText = Math.round((brightSlider.value / 255) * 100) + '%';
            document.getElementById('speedVal').innerText = speedSlider.value;
            document.getElementById('glowVal').innerText = glowSlider.value;
            document.getElementById('fadeVal').innerText = fadeSlider.value;
            
            // Update brightness track gradient
            brightSlider.style.setProperty('--track-bg', `linear-gradient(to right, #000, ${currentColorHex})`);
            
            // For webkit styles injection
            const style = document.createElement('style');
            style.innerHTML = `#brightness::-webkit-slider-runnable-track { background: linear-gradient(to right, #222, ${currentColorHex}) !important; }`;
            document.head.appendChild(style);
        }

        function setActiveColorBtn(name) {
            document.querySelectorAll('.color-btn').forEach(btn => {
                if(btn.dataset.name === name) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
        }

        // Network Comms via MQTT
        const DEVICE_MAC = prompt("Enter Device ID (MAC Address):", "A1B2C3") || "A1B2C3";
        const TOPIC_STATUS = `followme/${DEVICE_MAC}/status`;
        const TOPIC_RADAR = `followme/${DEVICE_MAC}/radar`;
        const TOPIC_CMD = `followme/${DEVICE_MAC}/cmd`;
        
        const client = mqtt.connect('wss://broker.hivemq.com:8884/mqtt');

        client.on('connect', () => {
            console.log('Connected to HiveMQ Cloud');
            client.subscribe(TOPIC_STATUS);
            client.subscribe(TOPIC_RADAR);
            statusDot.classList.add('connected');
            isConnected = true;
            showToast("Cloud Connected");
        });

        client.on('close', () => {
            statusDot.classList.remove('connected');
            isConnected = false;
        });

        client.on('message', (topic, message) => {
            try {
                const data = JSON.parse(message.toString());
                if (topic === TOPIC_STATUS) {
                    if(data.brightness !== undefined) brightSlider.value = data.brightness;
                    if(data.speed !== undefined) speedSlider.value = data.speed;
                    if(data.glowSize !== undefined) glowSlider.value = data.glowSize;
                    if(data.fadeSigma !== undefined) fadeSlider.value = data.fadeSigma;
                    if(data.colorMode) {
                        const preset = colorPresets.find(p => p.name === data.colorMode);
                        if(preset) {
                            currentColorHex = preset.ui;
                            setActiveColorBtn(data.colorMode);
                        }
                    }
                    updateUI();
                } else if (topic === TOPIC_RADAR) {
                    if(data.minGate !== undefined) minGateSlider.value = data.minGate;
                    if(data.maxGate !== undefined) maxGateSlider.value = data.maxGate;
                    if(data.timeout !== undefined) timeoutSlider.value = data.timeout;
                    if(data.motion) {
                        for(let i=0; i<5; i++) {
                            radarValues.m[i] = data.motion[i];
                            let track = document.querySelector(`.bar-track[data-type="m"][data-index="${i}"] .bar-fill`);
                            if(track) track.style.height = radarValues.m[i] + '%';
                        }
                    }
                    if(data.static) {
                        for(let i=0; i<5; i++) {
                            radarValues.s[i] = data.static[i];
                            let track = document.querySelector(`.bar-track[data-type="s"][data-index="${i}"] .bar-fill`);
                            if(track) track.style.height = radarValues.s[i] + '%';
                        }
                    }
                    updateRadarUI();
                }
            } catch (e) {
                console.error("Parse error:", e);
            }
        });

        let timeoutId;
        function sendUpdate(payload) {
            if (isConnected) {
                client.publish(TOPIC_CMD, JSON.stringify(payload));
            }
        }

        function throttledUpdate(payload) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => sendUpdate(payload), 100);
        }

        function showToast(msg = "Settings Saved") {
            toast.innerText = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2500);
        }

        // Radar Settings Logic
        const minGateSlider = document.getElementById('minGate');
        const maxGateSlider = document.getElementById('maxGate');
        const timeoutSlider = document.getElementById('timeout');
        
        let radarValues = {
            m: [50, 50, 50, 50, 50],
            s: [40, 40, 40, 40, 40]
        };

        function renderEq() {
            let html = '';
            for(let i=0; i<5; i++) {
                html += `
                <div class="gate-col">
                    <div class="bar-container">
                        <div class="bar-track" data-type="m" data-index="${i}">
                            <div class="bar-fill motion" style="height: ${radarValues.m[i]}%"></div>
                        </div>
                        <div class="bar-track" data-type="s" data-index="${i}">
                            <div class="bar-fill static" style="height: ${radarValues.s[i]}%"></div>
                        </div>
                    </div>
                    <div class="gate-label">${(i*0.75).toFixed(1)}m</div>
                </div>
                `;
            }
            document.getElementById('eqContainer').innerHTML = html;

            document.querySelectorAll('.bar-track').forEach(track => {
                let isDragging = false;
                
                function updateValue(e) {
                    const rect = track.getBoundingClientRect();
                    let y = e.clientY - rect.top;
                    let percent = 100 - (y / rect.height * 100);
                    if (percent < 0) percent = 0;
                    if (percent > 100) percent = 100;
                    
                    let val = Math.round(percent);
                    let type = track.getAttribute('data-type');
                    let idx = parseInt(track.getAttribute('data-index'));
                    radarValues[type][idx] = val;
                    track.querySelector('.bar-fill').style.height = val + '%';
                }

                track.addEventListener('pointerdown', e => {
                    isDragging = true;
                    track.setPointerCapture(e.pointerId);
                    updateValue(e);
                });
                track.addEventListener('pointermove', e => {
                    if (isDragging) updateValue(e);
                });
                track.addEventListener('pointerup', e => {
                    isDragging = false;
                    track.releasePointerCapture(e.pointerId);
                });
            });
        }
        renderEq();

        function toggleAdvanced() {
            const panel = document.getElementById('advPanel');
            const arrow = document.getElementById('advArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerText = '▲';
            } else {
                panel.style.display = 'none';
                arrow.innerText = '▼';
            }
        }

        function toggleRadar() {
            const panel = document.getElementById('radarPanel');
            const arrow = document.getElementById('radarArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerText = '▲';
            } else {
                panel.style.display = 'none';
                arrow.innerText = '▼';
            }
        }

        function updateRadarUI() {
            document.getElementById('minGateVal').innerText = (minGateSlider.value * 0.75).toFixed(2) + 'm';
            document.getElementById('maxGateVal').innerText = (maxGateSlider.value * 0.75).toFixed(2) + 'm';
            document.getElementById('timeoutVal').innerText = timeoutSlider.value + 's';
        }

        function applyRadarSettings() {
            const payload = {
                type: 'radar',
                minGate: parseInt(minGateSlider.value),
                maxGate: parseInt(maxGateSlider.value),
                timeout: parseInt(timeoutSlider.value)
            };
            for(let i=0; i<5; i++) {
                payload['m'+i] = radarValues.m[i];
                payload['s'+i] = radarValues.s[i];
            }
            sendUpdate(payload);
            showToast("Radar Command Sent to Cloud");
        }

        minGateSlider.addEventListener('input', updateRadarUI);
        maxGateSlider.addEventListener('input', updateRadarUI);
        timeoutSlider.addEventListener('input', updateRadarUI);

        // Event Listeners for Sliders
        const sliders = [
            { el: brightSlider, key: 'brightness' },
            { el: speedSlider, key: 'speed' },
            { el: glowSlider, key: 'glowSize' },
            { el: fadeSlider, key: 'fadeSigma' }
        ];

        sliders.forEach(s => {
            s.el.addEventListener('input', () => {
                updateUI();
                throttledUpdate({ [s.key]: parseInt(s.el.value) });
            });
        });

        // Color Selection
        window.selectColor = function(name, r, g, b, uiHex) {
            currentColorHex = uiHex;
            setActiveColorBtn(name);
            updateUI();
            sendUpdate({ colorMode: name, r: r, g: g, b: b });
            showToast("Color Sent");
        }
        
        window.applyRadarSettings = applyRadarSettings;
        window.toggleAdvanced = toggleAdvanced;
        window.toggleRadar = toggleRadar;