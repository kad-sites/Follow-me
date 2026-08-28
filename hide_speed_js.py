import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Modify setTvEffect
setTvEffect_old = """            if (effect === 'custom') {
                document.getElementById('customSeqPanel').style.display = 'block';
            } else {
                document.getElementById('customSeqPanel').style.display = 'none';
            }"""
setTvEffect_new = """            if (effect === 'custom') {
                document.getElementById('customSeqPanel').style.display = 'block';
                document.getElementById('effectSpeedBlock').style.display = 'none';
            } else {
                document.getElementById('customSeqPanel').style.display = 'none';
                document.getElementById('effectSpeedBlock').style.display = 'block';
            }"""
js = js.replace(setTvEffect_old, setTvEffect_new)

# Modify the sync from MQTT (when loading state)
sync_old = """                      if (tvEffect === 'custom') {
                          document.getElementById('customSeqPanel').style.display = 'block';
                      } else {
                          document.getElementById('customSeqPanel').style.display = 'none';
                      }"""
sync_new = """                      if (tvEffect === 'custom') {
                          document.getElementById('customSeqPanel').style.display = 'block';
                          document.getElementById('effectSpeedBlock').style.display = 'none';
                      } else {
                          document.getElementById('customSeqPanel').style.display = 'none';
                          document.getElementById('effectSpeedBlock').style.display = 'block';
                      }"""
js = js.replace(sync_old, sync_new)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
