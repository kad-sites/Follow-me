# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Reduce thumb size
html = html.replace("--thumb-size: 24px;", "--thumb-size: 16px;")

# 2. Reduce slider track thickness
html = html.replace("height: 6px; /* thinner track */", "height: 3px;")

# 3. Reduce slider container padding
html = html.replace("""        .slider-container {
            width: 100%;
            padding: 4px 0;
        }""", """        .slider-container {
            width: 100%;
            padding: 2px 0;
        }""")

# 4. Reduce section padding
old_section = """        .section {
            margin-bottom: 4px; margin-bottom: 4px; padding: 8px 16px; 
            background: var(--card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 12px;
            padding: 12px 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border);
            width: 100%;
            max-width: 450px;
        }"""
new_section = """        .section {
            margin-bottom: 4px;
            background: var(--card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 10px;
            padding: 6px 14px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border);
            width: 100%;
            max-width: 450px;
        }"""
html = html.replace(old_section, new_section)

# 5. Reduce section header margin
old_header = """        .section-header {
            display: flex;
            margin-bottom: 4px;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2px; /* Tighter margin */
        }"""
new_header = """        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0px;
        }"""
html = html.replace(old_header, new_header)

# 6. Reduce Power Buttons Size
# Pixora Power button
old_px_pwr = """<button id="pxPowerBtn" onclick="togglePxPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; height: 32px; padding: 0 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s; box-sizing: border-box;">ON</button>"""
new_px_pwr = """<button id="pxPowerBtn" onclick="togglePxPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 4px; height: 24px; padding: 0 12px; font-size: 11px; font-weight: bold; cursor: pointer; transition: all 0.2s; box-sizing: border-box;">ON</button>"""
html = html.replace(old_px_pwr, new_px_pwr)

# TV Power button
old_tv_pwr = """<button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; height: 32px; padding: 0 20px; font-size: 13px; font-weight: bold; cursor: pointer; transition: all 0.2s; box-sizing: border-box;">
                    ON
                </button>"""
new_tv_pwr = """<button id="tvPowerBtn" onclick="toggleTvPower()" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 4px; height: 24px; padding: 0 12px; font-size: 11px; font-weight: bold; cursor: pointer; transition: all 0.2s; box-sizing: border-box;">ON</button>"""
html = html.replace(old_tv_pwr, new_tv_pwr)

# Also fix the margin on the Pixora power div
html = html.replace("""<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">""", """<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">""")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("UI slimmed down!")
