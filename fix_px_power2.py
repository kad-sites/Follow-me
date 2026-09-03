with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

old_regex = r"function togglePxPower\(\)\s*\{\s*sendPxUpdate\(\);\s*\}"

new_toggle = """function togglePxPower() {
            pxIsOn = !pxIsOn;
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
            sendPxUpdate();
        }"""

js = re.sub(old_regex, new_toggle, js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
