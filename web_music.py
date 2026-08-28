import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_buttons = """                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'fire')">Fire Effect</button>
                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'custom')">Custom Sequence</button>
                    
                    <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 6px 0;"></div>
                    <span style="font-size: 11px; color: var(--subtext); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; padding-left: 8px;">Audio Sync</span>
                    
                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'music_pulse')">?? Pulse to Beat</button>
                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'music_meter')">?? Volume Meter</button>"""

html = html.replace("""                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'fire')">Fire Effect</button>
                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'custom')">Custom Sequence</button>""", new_buttons)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
