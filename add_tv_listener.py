with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

tv_listener = """
        const tvBrightEl = document.getElementById('tvBrightness');
        if (tvBrightEl) {
            tvBrightEl.addEventListener('input', (e) => {
                const v = e.target.value;
                const pct = Math.round((v / 255) * 100);
                document.getElementById('tvBrightVal').innerText = pct + '%';
                
                const min = e.target.min || 0;
                const max = e.target.max || 100;
                const percentage = ((v - min) / (max - min)) * 100;
                e.target.style.background = `linear-gradient(to right, rgb(${tvColor.r}, ${tvColor.g}, ${tvColor.b}) ${percentage}%, #333 ${percentage}%)`;
            });
            tvBrightEl.addEventListener('change', () => {
                sendTvUpdate();
            });
        }
"""

js = js.replace("window.toggleRadar = toggleRadar;", tv_listener + "\n        window.toggleRadar = toggleRadar;")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
