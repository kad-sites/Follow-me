import re
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add an ID to the Effect Speed label
html = html.replace('<div class="section-title">Effect Speed</div>', '<div class="section-title" id="speedLabel">Effect Speed</div>')
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Dynamically change the label text
old_js = r"if\(btn\) btn\.classList\.add\('active'\);\n\s*tvEffect = effect;"
new_js = """if(btn) btn.classList.add('active');
              tvEffect = effect;
              let lbl = document.getElementById('speedLabel');
              if (lbl) {
                  if (effect === 'music_pulse' || effect === 'music_meter') {
                      lbl.innerText = 'Audio Sensitivity';
                  } else {
                      lbl.innerText = 'Effect Speed';
                  }
              }"""
js = re.sub(old_js, new_js, js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
