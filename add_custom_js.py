import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. State vars
js = js.replace('let tvPixels = 27;', 'let tvPixels = 27;\n        let cSeg = 4;\n        let cSeqStr = "1, 2, 3, 4";\n        let cDel = 500;\n        let cAcc = false;')

# 2. Add visibility toggle in toggleTvEffect or when tvEffect changes
tv_eff_update = """        function setTvEffect(btn, effect) {
            tvEffect = effect;
            document.querySelectorAll('.tv-effect-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('tvEffectContent').style.display = 'none';
            if (effect === 'custom') {
                document.getElementById('customSeqPanel').style.display = 'block';
            } else {
                document.getElementById('customSeqPanel').style.display = 'none';
            }
            if (isConnected) throttledTvUpdate();
        }"""
js = re.sub(r'function setTvEffect.*?throttledTvUpdate\(\);\s*\}', tv_eff_update, js, flags=re.DOTALL)

# 3. Add Event listeners
js_listeners = """
        document.getElementById('cSeg').addEventListener('input', (e) => {
            cSeg = parseInt(e.target.value);
            document.getElementById('cSegVal').innerText = cSeg;
            if (isConnected) throttledTvUpdate();
        });
        document.getElementById('cDel').addEventListener('input', (e) => {
            cDel = parseInt(e.target.value);
            document.getElementById('cDelVal').innerText = (cDel / 1000).toFixed(1) + 's';
            if (isConnected) throttledTvUpdate();
        });
        document.getElementById('cAcc').addEventListener('change', (e) => {
            cAcc = e.target.checked;
            if (isConnected) throttledTvUpdate();
        });
        document.getElementById('cSeqStr').addEventListener('change', (e) => {
            cSeqStr = e.target.value;
            if (isConnected) throttledTvUpdate();
        });
"""
js = js.replace("let tvTimeoutId;", js_listeners + "let tvTimeoutId;")

# 4. Add to MQTT payload
payload_old = """                pixels: tvPixels,
                brightness: b,
                r: tvColor.r,"""
payload_new = """                pixels: tvPixels,
                brightness: b,
                r: tvColor.r,"""
# Actually, I'll inject at the bottom of the sendTvUpdate function
payload_update = """            
            if (tvEffect === 'custom') {
                payload.c_seg = cSeg;
                payload.c_del = cDel;
                payload.c_acc = cAcc;
                payload.c_seq = cSeqStr.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
            }
            
            client.publish(tvCmdTopic,"""
js = js.replace('client.publish(tvCmdTopic,', payload_update)

# 5. Add to sync from MQTT
sync_logic = """                  if (data.effect !== undefined) {
                      tvEffect = data.effect;
                      document.querySelectorAll('.tv-effect-btn').forEach(btn => {
                          if (btn.textContent.toLowerCase().includes(tvEffect)) btn.classList.add('active');
                          else btn.classList.remove('active');
                      });
                      if (tvEffect === 'custom') {
                          document.getElementById('customSeqPanel').style.display = 'block';
                      } else {
                          document.getElementById('customSeqPanel').style.display = 'none';
                      }
                  }"""
js = re.sub(r'if \(data\.effect !== undefined\).*?\}', sync_logic, js, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
