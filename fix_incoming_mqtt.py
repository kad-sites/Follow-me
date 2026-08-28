import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

old_code = """                    if (data.speed !== undefined) {
                        tvSpeed = data.speed;
                        document.getElementById('tvSpeed').value = tvSpeed;
                        document.getElementById('tvSpeedVal').innerText = tvSpeed + '%';
                    }"""

new_code = """                    if (data.speed !== undefined) {
                        tvSpeed = data.speed;
                        document.getElementById('tvSpeed').value = tvSpeed;
                        document.getElementById('tvSpeedVal').innerText = tvSpeed + '%';
                    }
                    if (data.pixels !== undefined) {
                        tvPixels = data.pixels;
                        document.getElementById('tvPixels').value = tvPixels;
                    }
                    if (data.c_seg !== undefined) {
                        cSeg = data.c_seg;
                        document.getElementById('cSeg').value = cSeg;
                        document.getElementById('cSegVal').innerText = cSeg;
                    }
                    if (data.c_del !== undefined) {
                        cDel = data.c_del;
                        document.getElementById('cDel').value = cDel;
                        document.getElementById('cDelVal').innerText = (cDel / 1000).toFixed(1) + 's';
                    }
                    if (data.c_acc !== undefined) {
                        cAcc = data.c_acc;
                        document.getElementById('cAcc').checked = cAcc;
                    }
                    if (data.c_seq !== undefined) {
                        cSeqStr = data.c_seq.join('-');
                        document.getElementById('cSeqStr').value = cSeqStr;
                    }"""

js = js.replace(old_code, new_code)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
