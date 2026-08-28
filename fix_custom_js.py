import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

bad_payload = """            const payload = {
                state: tvPower ? "ON" : "OFF",
                effect: tvEffect,
                speed: tvSpeed,
                pixels: tvPixels,
                brightness: b,
                r: tvColor.r,
                g: tvColor.g,
                b: tvColor.b
            };
            client.publish("kad/tvbacklit/cmd/zoheb", JSON.stringify(payload), { retain: true });"""

good_payload = """            const payload = {
                state: tvPower ? "ON" : "OFF",
                effect: tvEffect,
                speed: tvSpeed,
                pixels: tvPixels,
                brightness: b,
                r: tvColor.r,
                g: tvColor.g,
                b: tvColor.b
            };
            
            if (tvEffect === 'custom') {
                payload.c_seg = cSeg;
                payload.c_del = cDel;
                payload.c_acc = cAcc;
                payload.c_seq = cSeqStr.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
            }
            
            client.publish("kad/tvbacklit/cmd/zoheb", JSON.stringify(payload), { retain: true });"""

js = js.replace(bad_payload, good_payload)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
