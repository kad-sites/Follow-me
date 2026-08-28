import re
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Replace the bad selector with the correct one
old_logic = """            const headerTitle = document.querySelector('.header h1');
            if (activeTab === 'tv') {
                headerTitle.innerHTML = 'TV Backlit <span style="font-weight: 300; opacity: 0.7;">Controller</span>';
            } else {
                headerTitle.innerHTML = 'Follow-Me <span style="font-weight: 300; opacity: 0.7;">Controller</span>';
            }"""

new_logic = """            const headerTitle = document.querySelector('.header .title');
            if (headerTitle) {
                if (activeTab === 'tv') {
                    headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">TV Backlight</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                } else {
                    headerTitle.innerHTML = '<span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 600; font-size: 20px; color: #fbbf24; letter-spacing: -0.5px;">Follow-Me</span><span style="font-family: -apple-system, BlinkMacSystemFont, \\'Segoe UI\\', Roboto, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 14px; color: rgba(255,255,255,0.4); letter-spacing: 0.5px; margin-left: 6px;">Controller</span>';
                }
            }"""

js = js.replace(old_logic, new_logic)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
