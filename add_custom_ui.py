import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add "Custom Sequence" button to TV Effect list
effect_btn = """<button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'fire')">Fire Effect</button>"""
new_btn = """<button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'custom')">Custom Sequence</button>"""
html = html.replace(effect_btn, effect_btn + "\n                    " + new_btn)

# 2. Add the customSeqPanel right below the TV Effect list container
panel_html = """
        <div class="section" id="customSeqPanel" style="display: none; padding: 12px 16px; margin-top: 8px;">
            <div class="section-title">Animation Studio</div>
            
            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-top: 12px; margin-bottom: 4px;">
                <span style="color:var(--subtext)">Number of Segments</span>
                <span id="cSegVal" style="color:#fff">4</span>
            </div>
            <input type="range" id="cSeg" min="2" max="16" value="4" style="width: 100%; margin-bottom: 12px;">
            
            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
                <span style="color:var(--subtext)">Sequence Order (e.g., 1,3,2,4)</span>
            </div>
            <input type="text" id="cSeqStr" value="1, 2, 3, 4" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.2); background: rgba(0,0,0,0.3); color: white; margin-bottom: 12px; font-family: monospace;">
            
            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
                <span style="color:var(--subtext)">Step Delay (seconds)</span>
                <span id="cDelVal" style="color:#fff">0.5s</span>
            </div>
            <input type="range" id="cDel" min="50" max="2000" value="500" step="50" style="width: 100%; margin-bottom: 16px;">
            
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #fff;">
                <span>Accumulate Segments (Keep lit)</span>
                <label style="position:relative; display:inline-block; width:44px; height:24px;">
                    <input type="checkbox" id="cAcc" style="opacity:0; width:0; height:0;">
                    <span class="slider" style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:#333; transition:.4s; border-radius:24px;"></span>
                </label>
            </div>
        </div>
"""
# insert before <div class="toast" id="toast">
html = html.replace('<div class="toast"', panel_html + '\n    <div class="toast"')

# Add slider CSS
slider_css = """        input:checked + .slider { background-color: #fbbf24; }
        input:focus + .slider { box-shadow: 0 0 1px #fbbf24; }
        input:checked + .slider:before { transform: translateX(20px); }
        .slider:before { position: absolute; content: ""; height: 16px; width: 16px; left: 4px; bottom: 4px; background-color: white; transition: .4s; border-radius: 50%; }"""
html = html.replace('</style>', slider_css + '\n    </style>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
