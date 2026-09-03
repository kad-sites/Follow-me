with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

px_sync = """                } else if (topic === TOPIC_PX_STATUS) {
                    if (data.power !== undefined) {
                        pxIsOn = data.power;
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
                        const el = document.getElementById('pxBrightness');
                        if(el) { el.value = data.brightness; }
                    }
                    if (data.speed !== undefined) {
                        const el = document.getElementById('pxSpeed');
                        if(el) { el.value = data.speed; }
                    }
                    if (data.effect !== undefined) {
                        pxEffect = data.effect;
                        document.querySelectorAll('.px-effect-btn').forEach(b => {
                            b.classList.remove('active');
                            if(b.getAttribute('onclick') && b.getAttribute('onclick').includes("'" + pxEffect + "'")) {
                                b.classList.add('active');
                            }
                        });
                    }
"""

js = js.replace("} else if (topic === TOPIC_STATUS) {", px_sync + "                } else if (topic === TOPIC_STATUS) {")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
