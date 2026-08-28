import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace Sequence Order label and input
old_seq = """            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
                <span style="color:var(--subtext)">Sequence Order (e.g., 1,3,2,4)</span>
            </div>
            <input type="text" id="cSeqStr" value="1, 2, 3, 4" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.2); background: rgba(0,0,0,0.3); color: white; margin-bottom: 12px; font-family: monospace;">"""

new_seq = """            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
                <span style="color:var(--subtext)">Sequence Order</span>
            </div>
            <input type="text" id="cSeqStr" value="1-2-3-4" placeholder="e.g. 1-3-2-4" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.2); background: rgba(0,0,0,0.3); color: white; margin-bottom: 12px; font-family: monospace; font-size: 14px; letter-spacing: 2px;">"""

html = html.replace(old_seq, new_seq)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
