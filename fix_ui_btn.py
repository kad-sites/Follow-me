import re
with open("main.js", "r", encoding="utf-8") as f:
    code = f.read()

old_logic = r"if \(btn\.textContent\.toLowerCase\(\)\.includes\(tvEffect\)\) btn\.classList\.add\('active'\);\n\s*else btn\.classList\.remove\('active'\);"
new_logic = """let t = btn.textContent.toLowerCase();
                          let match = false;
                          if (tvEffect === 'music_pulse' && t.includes('pulse')) match = true;
                          else if (tvEffect === 'music_meter' && t.includes('meter')) match = true;
                          else if (tvEffect !== 'music_pulse' && tvEffect !== 'music_meter' && t.includes(tvEffect)) match = true;
                          if (match) btn.classList.add('active');
                          else btn.classList.remove('active');"""

code = re.sub(old_logic, new_logic, code)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(code)
