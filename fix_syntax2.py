import re
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

bad_block = """                 else {
                        headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">Follow-Me</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                    }
                }"""

html = html.replace(bad_block, "")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
