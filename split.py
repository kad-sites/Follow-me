import re
import os

path = r'C:\Users\ZOHEB\.gemini\antigravity\scratch\follow_me_dashboard\extracted_ui.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

script_start_idx = html.find('<script>')
script_end_idx = html.rfind('</script>')

if script_start_idx != -1 and script_end_idx != -1:
    css_and_html = html[:script_start_idx]
    original_js = html[script_start_idx+8:script_end_idx]
    
    new_html = css_and_html + '<script type="module" src="/main.js"></script>\n</body>\n</html>'
    
    with open(r'C:\Users\ZOHEB\.gemini\antigravity\scratch\follow_me_dashboard\index.html', 'w', encoding='utf-8') as f:
        f.write(new_html.strip())
        
    with open(r'C:\Users\ZOHEB\.gemini\antigravity\scratch\follow_me_dashboard\main.js', 'w', encoding='utf-8') as f:
        f.write(original_js.strip())
    
    print('Split successful')
else:
    print('Failed to split')
