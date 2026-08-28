import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add tvPixels state
js = js.replace('let tvSpeed = 50;', 'let tvSpeed = 50;\n        let tvPixels = 27;')

# Add event listener
listeners_old = """        document.getElementById('tvSpeed').addEventListener('input', (e) => {
            tvSpeed = parseInt(e.target.value);
            document.getElementById('tvSpeedVal').innerText = tvSpeed + "%";
            sendTvUpdate();
        });"""
listeners_new = """        document.getElementById('tvSpeed').addEventListener('input', (e) => {
            tvSpeed = parseInt(e.target.value);
            document.getElementById('tvSpeedVal').innerText = tvSpeed + "%";
            sendTvUpdate();
        });
        
        document.getElementById('tvPixels').addEventListener('input', (e) => {
            tvPixels = parseInt(e.target.value);
            document.getElementById('tvPixelsVal').innerText = tvPixels;
            sendTvUpdate();
        });"""
js = js.replace(listeners_old, listeners_new)

# Add to payload
payload_old = """                speed: tvSpeed,
                brightness: b,"""
payload_new = """                speed: tvSpeed,
                pixels: tvPixels,
                brightness: b,"""
js = js.replace(payload_old, payload_new)

# Add to MQTT sync logic
sync_old = """                  if (data.speed !== undefined) {
                      tvSpeed = data.speed;
                      document.getElementById('tvSpeed').value = tvSpeed;
                      document.getElementById('tvSpeedVal').innerText = tvSpeed + '%';
                  }"""
sync_new = """                  if (data.speed !== undefined) {
                      tvSpeed = data.speed;
                      document.getElementById('tvSpeed').value = tvSpeed;
                      document.getElementById('tvSpeedVal').innerText = tvSpeed + '%';
                  }
                  if (data.pixels !== undefined) {
                      tvPixels = data.pixels;
                      document.getElementById('tvPixels').value = tvPixels;
                      document.getElementById('tvPixelsVal').innerText = tvPixels;
                  }"""
js = js.replace(sync_old, sync_new)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
