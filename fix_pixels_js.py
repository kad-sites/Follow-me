with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Update the tvPixels listener from range to number input
old_listener = """        document.getElementById('tvPixels').addEventListener('input', (e) => {
            tvPixels = parseInt(e.target.value);
            document.getElementById('tvPixelsVal').innerText = tvPixels;
            if (isConnected) throttledTvUpdate();
        });"""

new_listener = """        document.getElementById('tvPixels').addEventListener('change', (e) => {
            let v = parseInt(e.target.value);
            if (isNaN(v) || v < 10) v = 10;
            if (v > 300) v = 300;
            e.target.value = v;
            tvPixels = v;
            if (isConnected) throttledTvUpdate();
        });"""

js = js.replace(old_listener, new_listener)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
