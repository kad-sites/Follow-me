with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

old_logic = """if (effect === 'music_pulse' || effect === 'music_meter') {
                      lbl.innerText = 'Audio Sensitivity';
                  } else {
                      lbl.innerText = 'Effect Speed';
                  }"""
new_logic = """if (effect === 'music_pulse' || effect === 'music_meter') {
                      lbl.innerText = 'Audio Sensitivity';
                      if (document.getElementById('tvTempBlock')) document.getElementById('tvTempBlock').style.display = 'none';
                  } else {
                      lbl.innerText = 'Effect Speed';
                      if (document.getElementById('tvTempBlock')) document.getElementById('tvTempBlock').style.display = 'block';
                  }"""
js = js.replace(old_logic, new_logic)

old_incoming = """if (tvEffect === 'music_pulse' || tvEffect === 'music_meter') lbl.innerText = 'Audio Sensitivity';
                            else lbl.innerText = 'Effect Speed';"""
new_incoming = """if (tvEffect === 'music_pulse' || tvEffect === 'music_meter') {
                                lbl.innerText = 'Audio Sensitivity';
                                if (document.getElementById('tvTempBlock')) document.getElementById('tvTempBlock').style.display = 'none';
                            } else {
                                lbl.innerText = 'Effect Speed';
                                if (document.getElementById('tvTempBlock')) document.getElementById('tvTempBlock').style.display = 'block';
                            }"""
js = js.replace(old_incoming, new_incoming)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
