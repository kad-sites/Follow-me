# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_tab_btn = """        .tab-btn {
            flex: 1;
            padding: 12px;
            background: transparent;
            color: var(--subtext);
            border: none;
            font-size: 14px;"""

new_tab_btn = """        .tab-btn {
            flex: 1;
            padding: 6px;
            background: transparent;
            color: var(--subtext);
            border: none;
            font-size: 12px;"""

old_tabs = """        .tabs {
            display: flex;
            max-width: 450px;
            width: 100%;
            background: var(--card);
            border-radius: 12px;"""

new_tabs = """        .tabs {
            display: flex;
            max-width: 450px;
            width: 100%;
            background: var(--card);
            border-radius: 8px;"""

if old_tab_btn in html:
    html = html.replace(old_tab_btn, new_tab_btn)
    html = html.replace(old_tabs, new_tabs)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Tabs slimmed down!")
else:
    print("Could not find old_tab_btn")
