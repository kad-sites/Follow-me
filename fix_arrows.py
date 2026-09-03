# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix HTML arrows
html = html.replace('style="color: var(--subtext); font-size: 12px;">&#9660;', 'style="color: var(--accent); font-size: 12px;">&#9660;')
html = html.replace('id="advArrow">&#9660;', 'id="advArrow" style="color: var(--accent);">&#9660;')

# Fix SVG arrows (chevrons)
# tvColorChevron
html = html.replace('<svg id="tvColorChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s; transform: rotate(180deg);">',
                    '<svg id="tvColorChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s; transform: rotate(180deg);">')

# tvEffectChevron
html = html.replace('<svg id="tvEffectChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s;">',
                    '<svg id="tvEffectChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s;">')

# pxColorChevron
html = html.replace('<svg id="pxColorChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s; transform: rotate(0deg);">',
                    '<svg id="pxColorChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s; transform: rotate(0deg);">')

# pxEffectChevron
html = html.replace('<svg id="pxEffectChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s;">',
                    '<svg id="pxEffectChevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.3s;">')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Arrows colored orange!")
