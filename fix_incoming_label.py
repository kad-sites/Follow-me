import re
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

old_incoming = r"document\.querySelectorAll\('\.tv-effect-btn'\)\.forEach\(btn => \{"
new_incoming = """let lbl = document.getElementById('speedLabel');
                        if (lbl) {
                            if (tvEffect === 'music_pulse' || tvEffect === 'music_meter') lbl.innerText = 'Audio Sensitivity';
                            else lbl.innerText = 'Effect Speed';
                        }
                        document.querySelectorAll('.tv-effect-btn').forEach(btn => {"""
js = js.replace(old_incoming, new_incoming)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
