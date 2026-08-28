import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Google font
if 'fonts.googleapis.com' not in html:
    html = html.replace('<head>', '<head>\n    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,900;1,900&display=swap" rel="stylesheet">')

old_title = """        <div class="title" style="font-weight: 800; font-size: 20px; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px; font-family: 'Segoe UI', system-ui, sans-serif;">
            <span class="status-dot" id="statusDot"></span>
            <span style="background: linear-gradient(to right, #f59e0b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 2px 10px rgba(245,158,11,0.2);">FOLLOW-ME</span>
            <span style="font-weight: 400; font-size: 12px; color: rgba(255,255,255,0.4); letter-spacing: 2px; text-transform: uppercase; margin-left: -2px;">Control</span>
        </div>"""

new_title = """        <div class="title" style="display: flex; align-items: center; gap: 4px;">
            <span style="font-family: 'Montserrat', sans-serif; font-weight: 900; font-style: italic; font-size: 22px; letter-spacing: 1px; background: linear-gradient(to right, #f59e0b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 2px 10px rgba(245,158,11,0.2);">FOLLOW-ME</span>
            <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-weight: 400; font-size: 12px; color: rgba(255,255,255,0.4); letter-spacing: 2px; text-transform: uppercase;">Control</span>
        </div>"""

html = html.replace(old_title, new_title)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
