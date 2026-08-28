import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_listeners = """        liveSliders.forEach(s => {
            if (s.el) {
                // Use 'change' so it fires when user lifts their finger
                s.el.addEventListener('change', () => {
                    let payload = {};
                    payload[s.key] = parseInt(s.el.value);
                    sendUpdate(payload);
                    showToast("Setting updated live");
                });
            }
        });"""

new_listeners = """        liveSliders.forEach(s => {
            if (s.el) {
                // Use 'change' so it fires when user lifts their finger
                s.el.addEventListener('change', () => {
                    let payload = {};
                    payload[s.key] = parseInt(s.el.value);
                    if (s.key === 'minDist' || s.key === 'maxDist' || s.key === 'timeout') {
                        payload['type'] = 'radar';
                    }
                    sendUpdate(payload);
                    showToast("Setting updated live");
                });
            }
        });"""

js = js.replace(old_listeners, new_listeners)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
