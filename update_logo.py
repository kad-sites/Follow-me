import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# remove google fonts import
html = re.sub(r'\s*<link href="https://fonts\.googleapis\.com/css2\?family=Montserrat[^>]*>', '', html)

old_title = """        <div class="title" style="display: flex; align-items: center; gap: 4px;">
            <span style="font-family: 'Montserrat', sans-serif; font-weight: 900; font-style: italic; font-size: 22px; letter-spacing: 1px; background: linear-gradient(to right, #f59e0b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 2px 10px rgba(245,158,11,0.2);">FOLLOW-ME</span>
            <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-weight: 400; font-size: 12px; color: rgba(255,255,255,0.4); letter-spacing: 2px; text-transform: uppercase;">Control</span>
        </div>"""

new_title = """        <div class="title" style="display: flex; align-items: baseline; gap: 6px;">
            <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">Follow-Me</span>
            <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px;">Controller</span>
        </div>"""

html = html.replace(old_title, new_title)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
