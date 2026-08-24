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
        
        let colorTarget = 'follow'; // 'follow' or 'base'
        let followColorHex = "#ff9329";
        let baseColorHex = "#ff9329";

        let isConnected = false;

        let activeTab = 'corridor';
        let tvColor = { r: 255, g: 147, b: 41 };
        let tvEffect = 'solid';
        let tvPower = true;
        let tvSpeed = 50;
        let tvPixels = 27;
        
        
        
        document.getElementById('tvSpeed').addEventListener('input', (e) => {
            tvSpeed = parseInt(e.target.value);
            document.getElementById('tvSpeedVal').innerText = tvSpeed + '%';
            if (isConnected) throttledTvUpdate();
        });
        document.getElementById('tvPixels').addEventListener('input', (e) => {
            tvPixels = parseInt(e.target.value);
            document.getElementById('tvPixelsVal').innerText = tvPixels;
            if (isConnected) throttledTvUpdate();
        });
        
        let tvTimeoutId;
        function throttledTvUpdate() {
            clearTimeout(tvTimeoutId);
            tvTimeoutId = setTimeout(sendTvUpdate, 100);
        }
        
function toggleTvPower() {
            tvPower = !tvPower;
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
            sendTvUpdate();
        }

        function switchTab(tabId) {
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
                state: tvPower ? "ON" : "OFF",
                effect: tvEffect,
                speed: tvSpeed,
                pixels: tvPixels,
                brightness: b,
                r: tvColor.r,
                g: tvColor.g,
                b: tvColor.b
            };
            client.publish("kad/tvbacklit/cmd/zoheb", JSON.stringify(payload), { retain: true });
            showToast("TV Sent");
        }

        
        // DOM Elements
        const statusDot = document.getElementById('statusDot');
        const fBrightSlider = document.getElementById('followBrightness');
        const bBrightSlider = document.getElementById('baseBrightness');
        const speedSlider = document.getElementById('followSpeed');
        const leadSlider = document.getElementById('leadFactor');
        const glowSlider = document.getElementById('glowSize');
        const fadeSlider = document.getElementById('fadeSigma');
        const pixelsSlider = document.getElementById('activePixels');
        const densitySlider = document.getElementById('ledDensity');
        const offsetSlider = document.getElementById('sensorOffset');
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
            document.getElementById('fBrightVal').innerText = Math.round((fBrightSlider.value / 255) * 100) + '%';
            document.getElementById('bBrightVal').innerText = Math.round((bBrightSlider.value / 255) * 100) + '%';
            document.getElementById('speedVal').innerText = speedSlider.value;
            if(leadSlider) document.getElementById('leadVal').innerText = leadSlider.value;
            document.getElementById('glowVal').innerText = glowSlider.value;
            document.getElementById('fadeVal').innerText = fadeSlider.value;
            if(pixelsSlider) document.getElementById('pixelsVal').innerText = pixelsSlider.value;
            if(densitySlider) document.getElementById('densityVal').innerText = densitySlider.value + ' LEDs/m';
            if(offsetSlider) document.getElementById('offsetVal').innerText = offsetSlider.value + ' cm';
            
            // Update brightness track gradient
            fBrightSlider.style.setProperty('--track-bg', `linear-gradient(to right, #000, ${followColorHex})`);
            bBrightSlider.style.setProperty('--track-bg', `linear-gradient(to right, #000, ${baseColorHex})`);
            
            // Glow width calculation (center out)
            const glowMin = parseInt(glowSlider.min) || 6;
            const glowMax = parseInt(glowSlider.max) || 60;
            const glowVal = parseInt(glowSlider.value);
            const glowP = (glowVal - glowMin) / (glowMax - glowMin);
            const halfP = (glowP * 100) / 2;
            const leftEdge = 50 - halfP;
            const rightEdge = 50 + halfP;
            
            // For webkit styles injection
            let style = document.getElementById('dynamic-slider-styles');
            if (!style) {
                style = document.createElement('style');
                style.id = 'dynamic-slider-styles';
                document.head.appendChild(style);
            }
            style.innerHTML = `
                #followBrightness::-webkit-slider-runnable-track { background: linear-gradient(to right, #222, ${followColorHex}) !important; }
                #baseBrightness::-webkit-slider-runnable-track { background: linear-gradient(to right, #222, ${baseColorHex}) !important; }
                #glowSize::-webkit-slider-runnable-track { background: linear-gradient(to right, #333 0%, #333 ${leftEdge}%, ${baseColorHex} 50%, #333 ${rightEdge}%, #333 100%) !important; }
            `;
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
        
        let DEVICE_MAC = localStorage.getItem('DEVICE_MAC');
        let TOPIC_STATUS, TOPIC_RADAR, TOPIC_CMD;
        
        const client = mqtt.connect('wss://broker.hivemq.com:8884/mqtt');

        function initCorridorConnection() {
            if (!DEVICE_MAC) {
                const overlay = document.getElementById('mac-overlay');
                if (overlay) overlay.style.display = 'flex';
                return;
            }
            const overlay = document.getElementById('mac-overlay');
            if (overlay) overlay.style.display = 'none';
            
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
            client.subscribe("kad/tvbacklit/cmd/zoheb");
            if(statusDot) statusDot.classList.add('connected');
            const err = document.getElementById('connErrorMsg');
            if (err) err.style.display = 'none';
            isConnected = true;
            showToast("Cloud Connected");
        });

        // call init on load
        setTimeout(initCorridorConnection, 100);


        client.on('close', () => {
            if(statusDot) statusDot.classList.remove('connected');
            document.getElementById('connErrorMsg').style.display = 'block';
            isConnected = false;
        });

        client.on('message', (topic, message) => {
            try {
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
                
                if (topic === TOPIC_STATUS) {
                    if(data.followBrightness !== undefined) fBrightSlider.value = data.followBrightness;
                    if(data.baseBrightness !== undefined) bBrightSlider.value = data.baseBrightness;
                    if(data.speed !== undefined) speedSlider.value = data.speed;
                    if(data.leadFactor !== undefined && leadSlider) leadSlider.value = data.leadFactor;
                    if(data.glowSize !== undefined) glowSlider.value = data.glowSize;
                    if(data.fadeSigma !== undefined) fadeSlider.value = data.fadeSigma;
                    if(data.activePixels !== undefined) if(pixelsSlider) pixelsSlider.value = data.activePixels;
                    if(data.ledDensity !== undefined && densitySlider) densitySlider.value = data.ledDensity;
                    if(data.sensorOffset !== undefined && offsetSlider) offsetSlider.value = data.sensorOffset;

                    if(data.fR !== undefined) followColorHex = `rgb(${data.fR},${data.fG},${data.fB})`;
                    if(data.bR !== undefined) baseColorHex = `rgb(${data.bR},${data.bG},${data.bB})`;
                    // color mode active button logic skipped for simplicity when splitting targets

                    updateUI();



                } else if (topic === TOPIC_RADAR) {
                    if(data.minDist !== undefined) minDistSlider.value = data.minDist;
                    if(data.maxDist !== undefined) maxDistSlider.value = data.maxDist;
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
        const minDistSlider = document.getElementById('minDist');
        const maxDistSlider = document.getElementById('maxDist');
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

        // Click outside to close Radar Panel
        document.addEventListener('click', (e) => {
            const panels = [
                { id: 'radarPanel', arrow: 'radarArrow', toggle: 'toggleRadar()' },
                { id: 'colorPanel', arrow: 'colorArrow', toggle: 'toggleColor()' },
                { id: 'calibPanel', arrow: 'calibArrow', toggle: 'toggleCalib()' },
                { id: 'pixelsPanel', arrow: 'pixelsArrow', toggle: 'togglePixels()' }
            ];
            
            panels.forEach(p => {
                const panel = document.getElementById(p.id);
                const arrow = document.getElementById(p.arrow);
                if (panel && panel.style.display === 'block') {
                    const clickedInside = e.target.closest('#' + p.id) || e.target.closest('[onclick="' + p.toggle + '"]');
                    if (!clickedInside) {
                        panel.style.display = 'none';
                        arrow.innerHTML = '&#9660;';
                    }
                }
            });
        });

        function toggleAdvanced() {
            const panel = document.getElementById('advPanel');
            const arrow = document.getElementById('advArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '&#9650;';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '&#9660;';
            }
        }

        function toggleRadar() {
            const panel = document.getElementById('radarPanel');
            const arrow = document.getElementById('radarArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '&#9650;';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '&#9660;';
            }
        }

        function toggleCalib() {
            const panel = document.getElementById('calibPanel');
            const arrow = document.getElementById('calibArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '&#9650;';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '&#9660;';
            }
        }

        function updateRadarUI() {
            document.getElementById('minDistVal').innerText = minDistSlider.value + 'cm';
            document.getElementById('maxDistVal').innerText = maxDistSlider.value + 'cm';
            document.getElementById('timeoutVal').innerText = timeoutSlider.value + 's';
        }

        

        minDistSlider.addEventListener('input', updateRadarUI);
        maxDistSlider.addEventListener('input', updateRadarUI);
        timeoutSlider.addEventListener('input', updateRadarUI);

        // Event Listeners for Sliders
        const sliders = [
            { el: fBrightSlider, key: 'followBrightness' },
            { el: bBrightSlider, key: 'baseBrightness' },
            { el: leadSlider, key: 'leadFactor' },
            { el: speedSlider, key: 'speed' },
            { el: glowSlider, key: 'glowSize' },
            { el: fadeSlider, key: 'fadeSigma' },
            { el: pixelsSlider, key: 'activePixels' },
            { el: densitySlider, key: 'ledDensity' },
            { el: offsetSlider, key: 'sensorOffset' }
        ];

                sliders.forEach(s => {
            if (s.el) {
                s.el.addEventListener('input', () => {
                    updateUI();
                    throttledUpdate({ [s.key]: parseInt(s.el.value) });
                });
            }
        });

        // Add live "change" listeners to all dropdown sliders so they send immediately
        const liveSliders = [
            { el: pixelsSlider, key: 'activePixels' },
            { el: densitySlider, key: 'ledDensity' },
            { el: offsetSlider, key: 'sensorOffset' },
            { el: minDistSlider, key: 'minDist' },
            { el: maxDistSlider, key: 'maxDist' },
            { el: timeoutSlider, key: 'timeout' }
        ];
        
        liveSliders.forEach(s => {
            if (s.el) {
                // Use 'change' so it fires when user lifts their finger
                s.el.addEventListener('change', () => {
                    let payload = {};
                    payload[s.key] = parseInt(s.el.value);
                    if (s.key === 'minDist' || s.key === 'maxDist' || s.key === 'timeout') {
                        payload['type'] = 'radar';
                    }
                    sendUpdate(payload);
                    showToast("Setting updated live");
                });
            }
        });

        // Color Selection
        window.selectColor = function(name, r, g, b, uiHex) {
            setActiveColorBtn(name);
            if (colorTarget === 'follow') {
                followColorHex = uiHex;
                sendUpdate({ fR: r, fG: g, fB: b });
            } else {
                baseColorHex = uiHex;
                sendUpdate({ bR: r, bG: g, bB: b });
            }
            updateUI();



            showToast("Color Sent to " + colorTarget);
        }
        
        window.setColorTarget = function(target) {
            colorTarget = target;
            const followBtn = document.getElementById('tgtFollowBtn');
            const baseBtn = document.getElementById('tgtBaseBtn');
            if (target === 'follow') {
                followBtn.style.background = 'transparent';
                followBtn.style.border = '1px solid #60a5fa';
                followBtn.style.color = '#fff';
                baseBtn.style.background = 'transparent';
                baseBtn.style.border = 'none';
                baseBtn.style.color = '#94a3b8';
            } else {
                baseBtn.style.background = 'transparent';
                baseBtn.style.border = '1px solid #60a5fa';
                baseBtn.style.color = '#fff';
                followBtn.style.background = 'transparent';
                followBtn.style.border = 'none';
                followBtn.style.color = '#94a3b8';
            }
        }

        
        
        window.promptPixelLimits = function() {
            let slider = document.getElementById('activePixels');
            let currentMin = slider.min;
            let currentMax = slider.max;
            
            let newMin = window.prompt("Enter Minimum Active Pixels:", currentMin);
            if (newMin !== null) {
                newMin = parseInt(newMin);
                if (!isNaN(newMin) && newMin > 0) {
                    slider.min = newMin;
                    document.getElementById('pixelsMinLabel').innerText = newMin;
                }
            }
            
            let newMax = window.prompt("Enter Maximum Active Pixels:", currentMax);
            if (newMax !== null) {
                newMax = parseInt(newMax);
                let currentSliderMin = parseInt(slider.min);
                if (!isNaN(newMax) && newMax > currentSliderMin) {
                    slider.max = newMax;
                    document.getElementById('pixelsMaxLabel').innerText = newMax;
                }
            }
            updateUI();



        }
        
        window.resetDeviceId = function() {
            localStorage.removeItem('DEVICE_MAC');
            location.reload();
        }
        
                function applyMainSettings() {
            const payload = {};
            sliders.forEach(s => {
                if (s.el) payload[s.key] = parseInt(s.el.value);
            });
            sendUpdate(payload);
            showToast("Settings Applied to Controller");
        }
        window.applyMainSettings = applyMainSettings;

        window.toggleAdvanced = toggleAdvanced;
                function togglePixels() {
            const panel = document.getElementById('pixelsPanel');
            const arrow = document.getElementById('pixelsArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '&#9650;';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '&#9660;';
            }
        }
        window.togglePixels = togglePixels;
        
        function toggleColor() {
            const panel = document.getElementById('colorPanel');
            const arrow = document.getElementById('colorArrow');
            if (panel.style.display === 'none') {
                panel.style.display = 'block';
                arrow.innerHTML = '&#9650;';
            } else {
                panel.style.display = 'none';
                arrow.innerHTML = '&#9660;';
            }
        }

        

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


        window.toggleRadar = toggleRadar;
        window.toggleColor = toggleColor;
        window.toggleCalib = toggleCalib;

        // TV tab functions
        window.switchTab = switchTab;
        window.toggleTvColor = toggleTvColor;
        window.toggleTvEffect = toggleTvEffect;
        window.setTvColor = setTvColor;
        window.setTvEffect = setTvEffect;
        window.sendTvUpdate = sendTvUpdate;
        window.toggleTvPower = toggleTvPower;

        // Restore tab on load
        const savedTab = localStorage.getItem('activeTab');
        if (savedTab) {
            switchTab(savedTab);
        }
