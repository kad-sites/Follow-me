# -*- coding: utf-8 -*-
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

old_on_msg = """                if (topic === "kad/tvbacklit/cmd/zoheb") {"""
new_on_msg = """                if (topic === TOPIC_PX_STATUS) {
                    if (data.power !== undefined || data.isOn !== undefined) {
                        pxIsOn = (data.power !== undefined) ? data.power : data.isOn;
                        const btn = document.getElementById('pxPowerBtn');
                        if (btn) {
                            if (pxIsOn) {
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
                    }
                    if (data.brightness !== undefined) {
                        const bEl = document.getElementById('pxBrightness');
                        if (bEl && document.activeElement !== bEl) {
                            bEl.value = data.brightness;
                            document.getElementById('pxBrightVal').innerText = Math.round((data.brightness / 255) * 100) + '%';
                        }
                    }
                    if (data.speed !== undefined) {
                        const sEl = document.getElementById('pxSpeed');
                        if (sEl && document.activeElement !== sEl) {
                            sEl.value = data.speed;
                            document.getElementById('pxSpeedVal').innerText = data.speed + '%';
                        }
                    }
                    if (data.effect !== undefined) {
                        pxEffect = data.effect;
                        document.querySelectorAll('.px-effect-btn').forEach(btn => {
                            if (btn.innerText.toLowerCase().includes(pxEffect.replace('_', ' ').split(' ')[0])) {
                                btn.classList.add('active');
                            } else if (pxEffect === 'solid' && btn.innerText.includes('Solid')) btn.classList.add('active');
                            else if (pxEffect === 'candy_crush' && btn.innerText.includes('Candy')) btn.classList.add('active');
                            else btn.classList.remove('active');
                        });
                    }
                    if (data.text !== undefined) {
                        pxText = data.text;
                        const tEl = document.getElementById('pxTextInput');
                        if (tEl && document.activeElement !== tEl) {
                            tEl.value = pxText;
                        }
                    }
                } else if (topic === "kad/tvbacklit/cmd/zoheb") {"""

if old_on_msg in js:
    js = js.replace(old_on_msg, new_on_msg)
    with open("main.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("Dashboard Sync fixed")
else:
    print("Could not find old_on_msg")
