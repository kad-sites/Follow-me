import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

speed_html = """            <div class="section-header">
                <div class="section-title">Effect Speed</div>
                <div class="value-display" id="tvSpeedVal">50%</div>
            </div>
            <div class="slider-container">
                <input type="range" id="tvSpeed" min="1" max="100" value="50" style="touch-action: pan-y;">
            </div>"""

wrapped_speed = """            <div id="effectSpeedBlock">
""" + speed_html + """
            </div>"""

html = html.replace(speed_html, wrapped_speed)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
