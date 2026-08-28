import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_header = """    <div class="header">
        <div class="title" style="font-weight: 600; font-size: 18px; display: flex; align-items: center; gap: 8px;">
            <span class="status-dot" id="statusDot"></span>
            Follow-Me Controller
        </div>
    </div>"""

new_header = """    <div class="header" style="flex-direction: column; align-items: center;">
        <div class="title" style="font-weight: 600; font-size: 18px; display: flex; align-items: center; gap: 8px;">
            <span class="status-dot" id="statusDot"></span>
            Follow-Me Controller
        </div>
        <div id="connErrorMsg" style="color: #ef4444; font-size: 11px; margin-top: 6px; display: block; opacity: 0.8;">Unable to connect to controller</div>
    </div>"""

html = html.replace(old_header, new_header)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
