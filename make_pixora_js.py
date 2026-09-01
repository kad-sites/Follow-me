import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Topics
topics = """
const TOPIC_TV_STATUS = "kad/tvbacklit/status/zoheb";
const TOPIC_PX_CMD = "kad/pixora/cmd/zoheb";
const TOPIC_PX_STATUS = "kad/pixora/status/zoheb";
"""
js = js.replace('const TOPIC_TV_STATUS = "kad/tvbacklit/status/zoheb";', topics)

# Subscribe to Pixora status
js = js.replace("client.subscribe(TOPIC_TV_STATUS);", "client.subscribe(TOPIC_TV_STATUS);\n                  client.subscribe(TOPIC_PX_STATUS);")

# Handle Tab switching logic
old_switchTab = """if (tabId === 'corridor') {
                  document.getElementById('btn-corridor').classList.add('active');
                  document.getElementById('tab-corridor').style.display = 'block';
              } else {
                  document.getElementById('btn-tv').classList.add('active');
                  document.getElementById('tab-tv').style.display = 'block';
              }"""
new_switchTab = """document.getElementById('btn-corridor').classList.remove('active');
              document.getElementById('btn-tv').classList.remove('active');
              document.getElementById('btn-pixora').classList.remove('active');
              document.getElementById('tab-corridor').style.display = 'none';
              document.getElementById('tab-tv').style.display = 'none';
              document.getElementById('tab-pixora').style.display = 'none';
              
              if (tabId === 'corridor') {
                  document.getElementById('btn-corridor').classList.add('active');
                  document.getElementById('tab-corridor').style.display = 'block';
              } else if (tabId === 'tv') {
                  document.getElementById('btn-tv').classList.add('active');
                  document.getElementById('tab-tv').style.display = 'block';
              } else if (tabId === 'pixora') {
                  document.getElementById('btn-pixora').classList.add('active');
                  document.getElementById('tab-pixora').style.display = 'block';
              }"""
js = js.replace(old_switchTab, new_switchTab)

# Pixora Variables
px_vars = """
          let pxEffect = 'solid';
          let pxR = 255, pxG = 147, pxB = 41;
          let pxIsOn = true;
"""
js = js.replace("let colorTarget = 'follow';", px_vars + "let colorTarget = 'follow';")


# Pixora Logic Functions
px_funcs = """
          function sendPxUpdate(extraPayload = {}) {
              if (isConnected) {
                  let payload = {
                      power: document.getElementById('pxPower') ? document.getElementById('pxPower').checked : true,
                      brightness: parseInt(document.getElementById('pxBrightness') ? document.getElementById('pxBrightness').value : 60),
                      speed: parseInt(document.getElementById('pxSpeed') ? document.getElementById('pxSpeed').value : 50),
                      effect: pxEffect,
                      r: pxR,
                      g: pxG,
                      b: pxB
                  };
                  Object.assign(payload, extraPayload);
                  client.publish(TOPIC_PX_CMD, JSON.stringify(payload));
              }
          }

          function togglePxPower() {
              sendPxUpdate();
          }

          function setPxColor(btn, r, g, b) {
              document.querySelectorAll('.px-color-btn').forEach(b => b.classList.remove('active'));
              if(btn) btn.classList.add('active');
              pxR = r; pxG = g; pxB = b;
              sendPxUpdate();
          }
          
          function setPxRandomColor() {
              document.querySelectorAll('.px-color-btn').forEach(b => b.classList.remove('active'));
              pxR = Math.floor(Math.random() * 256);
              pxG = Math.floor(Math.random() * 256);
              pxB = Math.floor(Math.random() * 256);
              sendPxUpdate({random_color: true});
          }

          function setPxEffect(btn, effect) {
              document.querySelectorAll('.px-effect-btn').forEach(b => {
                  b.classList.remove('active');
                  b.innerHTML = b.innerHTML.replace(' <span style="float:right">?</span>', '');
              });
              btn.classList.add('active');
              btn.innerHTML += ' <span style="float:right">?</span>';
              pxEffect = effect;
              sendPxUpdate();
          }

          function togglePxColor() {
              const content = document.getElementById('pxColorContent');
              const chevron = document.getElementById('pxColorChevron');
              content.classList.toggle('open');
              chevron.style.transform = content.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
          }

          function togglePxEffect() {
              const content = document.getElementById('pxEffectContent');
              const chevron = document.getElementById('pxEffectChevron');
              content.classList.toggle('open');
              chevron.style.transform = content.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
          }
          
          window.savePxSettings = function() {
              if (!isConnected) {
                  showToast("Not connected to MQTT");
                  return;
              }
              sendPxUpdate({save: true});
              showToast("Pixora Settings Saved!");
          }
"""

js = js.replace("// Restore tab on load", px_funcs + "\n          // Restore tab on load")

# Expose window functions
js = js.replace("window.toggleTvPower = toggleTvPower;", "window.toggleTvPower = toggleTvPower;\n          window.togglePxColor = togglePxColor;\n          window.togglePxEffect = togglePxEffect;\n          window.setPxColor = setPxColor;\n          window.setPxRandomColor = setPxRandomColor;\n          window.setPxEffect = setPxEffect;\n          window.savePxSettings = savePxSettings;\n          window.togglePxPower = togglePxPower;\n          window.sendPxUpdate = sendPxUpdate;")

# Live Sliders Pixora
new_live_sliders = """
              { el: document.getElementById('pxBrightness'), key: 'pxBrightness' },
              { el: document.getElementById('pxSpeed'), key: 'pxSpeed' },
"""
js = js.replace("{ el: document.getElementById('vrt'), key: 'vrt' },", "{ el: document.getElementById('vrt'), key: 'vrt' },\n" + new_live_sliders)


# Pixora Event Listeners
px_slider_listeners = """
          ['pxBrightness', 'pxSpeed'].forEach(id => {
              const el = document.getElementById(id);
              if (el) {
                  el.addEventListener('input', (e) => {
                      const valDisplay = document.getElementById(id + 'Val');
                      if (valDisplay) valDisplay.innerText = e.target.value + (id.includes('Speed')?'%':'');
                  });
                  el.addEventListener('change', () => {
                      sendPxUpdate();
                  });
              }
          });
"""
js = js.replace("// VU Meter Sliders (TV)", px_slider_listeners + "\n          // VU Meter Sliders (TV)")


# Message Parse
parse_px = """
              } else if (topic === TOPIC_PX_STATUS) {
                  try {
                      const data = JSON.parse(message.toString());
                      
                      if(data.power !== undefined && document.getElementById('pxPower')) {
                          document.getElementById('pxPower').checked = data.power;
                          pxIsOn = data.power;
                      }
                      
                      if(data.brightness !== undefined && document.getElementById('pxBrightness')) {
                          document.getElementById('pxBrightness').value = data.brightness;
                          document.getElementById('pxBrightVal').innerText = data.brightness;
                      }
                      
                      if(data.speed !== undefined && document.getElementById('pxSpeed')) {
                          document.getElementById('pxSpeed').value = data.speed;
                          document.getElementById('pxSpeedVal').innerText = data.speed + '%';
                      }
                      
                      if(data.effect !== undefined) {
                          pxEffect = data.effect;
                          document.querySelectorAll('.px-effect-btn').forEach(b => {
                              b.classList.remove('active');
                              b.innerHTML = b.innerHTML.replace(' <span style="float:right">?</span>', '');
                              if (b.getAttribute('onclick').includes(data.effect)) {
                                  b.classList.add('active');
                                  b.innerHTML += ' <span style="float:right">?</span>';
                              }
                          });
                      }
                  } catch (e) {
                      console.error("Error parsing Pixora status JSON", e);
                  }
              }
"""

js = js.replace('console.error("Error parsing TV status JSON", e);\n                  }\n              }', 'console.error("Error parsing TV status JSON", e);\n                  }\n' + parse_px + '\n              }')

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
