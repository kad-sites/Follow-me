import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Pull White Temperature out of tvColorContent
# Find the exact boundary
boundary = """                </div>
                <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 4px 0;"></div>
                <div class="section-header">
                    <div class="section-title">White Temperature</div>"""
new_boundary = """                </div>
            </div> <!-- End of tvColorContent -->
            
            <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 4px 0;"></div>
            <div class="section-header">
                <div class="section-title">White Temperature</div>"""
html = html.replace(boundary, new_boundary)

# Remove the old closing div for tvColorContent
# It was right before the tvEffectPanel section
old_ending = """                    </div>
                </div>

            </div>
        </div>

        <div class="section dropdown-panel" id="tvEffectPanel">"""
new_ending = """                    </div>
                </div>

        </div>

        <div class="section dropdown-panel" id="tvEffectPanel">"""
html = html.replace(old_ending, new_ending)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
    
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Implement accordion logic
js = js.replace("""        function toggleTvColor() {
            const content = document.getElementById('tvColorContent');
            const chev = document.getElementById('tvColorChevron');
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                chev.style.transform = 'rotate(0deg)';
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                chev.style.transform = 'rotate(180deg)';
            }
        }""", """        function toggleTvColor() {
            const content = document.getElementById('tvColorContent');
            const chev = document.getElementById('tvColorChevron');
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                chev.style.transform = 'rotate(0deg)';
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                chev.style.transform = 'rotate(180deg)';
                // Auto-close effect panel
                const effContent = document.getElementById('tvEffectContent');
                const effChev = document.getElementById('tvEffectChevron');
                if (effContent && effContent.style.maxHeight) {
                    effContent.style.maxHeight = null;
                    effChev.style.transform = 'rotate(0deg)';
                }
            }
        }""")

js = js.replace("""        function toggleTvEffect() {
            const content = document.getElementById('tvEffectContent');
            const chev = document.getElementById('tvEffectChevron');
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                chev.style.transform = 'rotate(0deg)';
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                chev.style.transform = 'rotate(180deg)';
            }
        }""", """        function toggleTvEffect() {
            const content = document.getElementById('tvEffectContent');
            const chev = document.getElementById('tvEffectChevron');
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                chev.style.transform = 'rotate(0deg)';
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                chev.style.transform = 'rotate(180deg)';
                // Auto-close color panel
                const colContent = document.getElementById('tvColorContent');
                const colChev = document.getElementById('tvColorChevron');
                if (colContent && colContent.style.maxHeight) {
                    colContent.style.maxHeight = null;
                    colChev.style.transform = 'rotate(0deg)';
                }
            }
        }""")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
