import re
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Remove the duplicates and vlb/vlt/vrb/vrt from liveSliders
js = re.sub(r'\{\s*el:\s*document\.getElementById\(\'vl[bt]\'\),\s*key:\s*\'vl[bt]\'\s*\},\n\s*', '', js)
js = re.sub(r'\{\s*el:\s*document\.getElementById\(\'vr[bt]\'\),\s*key:\s*\'vr[bt]\'\s*\},\n\s*', '', js)

# 2. Add proper listeners for the TV VU sliders
vu_listeners = """
          // VU Meter Sliders (TV)
          ['vlb', 'vlt', 'vrb', 'vrt'].forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                  el.addEventListener('input', (e) => {
                      const valDisplay = document.getElementById(id + 'Val');
                      if (valDisplay) valDisplay.innerText = e.target.value;
                  });
                  el.addEventListener('change', () => {
                      sendTvUpdate();
                  });
              }
          });
"""

# Inject before window.selectColor
js = js.replace('// Color Selection', vu_listeners + '\n          // Color Selection')

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
