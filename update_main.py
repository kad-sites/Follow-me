with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# Add pxText variable
js = js.replace("let pxEffect = 'solid';", "let pxEffect = 'solid';\n        let pxText = 'ZOHEB';")

# Add text listener (debounced)
text_listener = """
        let pxTextTimeout = null;
        const pxTextInput = document.getElementById('pxTextInput');
        if (pxTextInput) {
            pxTextInput.addEventListener('input', (e) => {
                pxText = e.target.value.substring(0, 30).toUpperCase(); // enforce upper case and limit length
                if (pxTextTimeout) clearTimeout(pxTextTimeout);
                pxTextTimeout = setTimeout(() => {
                    sendPxUpdate();
                }, 400); // 400ms debounce
            });
        }
"""
# insert near other px listeners
js = js.replace("['pxBrightness', 'pxSpeed'].forEach(id => {", text_listener + "\n        ['pxBrightness', 'pxSpeed'].forEach(id => {")

# Add text to payload
js = js.replace("effect: pxEffect,", "effect: pxEffect,\n                        text: pxText,")

# Sync incoming text status
sync_logic = """                    if (data.text !== undefined) {
                        pxText = data.text;
                        const el = document.getElementById('pxTextInput');
                        if (el && document.activeElement !== el) {
                            el.value = pxText;
                        }
                    }
"""
js = js.replace("if (data.effect !== undefined) {", sync_logic + "                    if (data.effect !== undefined) {")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
