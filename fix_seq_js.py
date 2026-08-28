import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Change default cSeqStr to dash format
js = js.replace('let cSeqStr = "1, 2, 3, 4";', 'let cSeqStr = "1-2-3-4";')

# 2. Update segment slider listener to auto-generate sequence
old_seg_listener = """        document.getElementById('cSeg').addEventListener('input', (e) => {
            cSeg = parseInt(e.target.value);
            document.getElementById('cSegVal').innerText = cSeg;
            if (isConnected) throttledTvUpdate();
        });"""

new_seg_listener = """        document.getElementById('cSeg').addEventListener('input', (e) => {
            cSeg = parseInt(e.target.value);
            document.getElementById('cSegVal').innerText = cSeg;
            // Auto-generate default sequence 1-2-3-...-N
            let seq = [];
            for (let i = 1; i <= cSeg; i++) seq.push(i);
            cSeqStr = seq.join('-');
            document.getElementById('cSeqStr').value = cSeqStr;
            if (isConnected) throttledTvUpdate();
        });"""

js = js.replace(old_seg_listener, new_seg_listener)

# 3. Update cSeqStr change listener to parse dashes
old_seq_listener = """        document.getElementById('cSeqStr').addEventListener('change', (e) => {
            cSeqStr = e.target.value;
            if (isConnected) throttledTvUpdate();
        });"""

new_seq_listener = """        document.getElementById('cSeqStr').addEventListener('change', (e) => {
            cSeqStr = e.target.value.replace(/,/g, '-').replace(/\\s+/g, '');
            e.target.value = cSeqStr;
            if (isConnected) throttledTvUpdate();
        });"""

js = js.replace(old_seq_listener, new_seq_listener)

# 4. Update the payload parser to split by dash instead of comma
old_parse = "payload.c_seq = cSeqStr.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));"
new_parse = "payload.c_seq = cSeqStr.split('-').map(s => parseInt(s.trim())).filter(n => !isNaN(n));"
js = js.replace(old_parse, new_parse)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
