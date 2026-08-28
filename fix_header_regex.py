import re
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

pattern = r"const headerTitle = document\.querySelector\('\.header h1'\);\s*if \(activeTab === 'tv'\) \{.*?\n\s*\} else \{.*?\n\s*\}"
replacement = """const headerTitle = document.querySelector('.header .title');
            if (headerTitle) {
                if (activeTab === 'tv') {
                    headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">TV Backlight</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                } else {
                    headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">Follow-Me</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                }
            }"""

js = re.sub(pattern, replacement, js, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
