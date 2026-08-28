with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace closing and opening section divs with just a separator
separator = '''
        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 16px 0;"></div>
'''

html = html.replace('    </div>\n\n    <!-- Follow Speed -->\n    <div class="section">', separator)
html = html.replace('    </div>\n\n    <!-- Glow Width -->\n    <div class="section">', separator)
html = html.replace('    </div>\n\n    <!-- Active Pixels -->\n    <div class="section">', separator)
html = html.replace('    </div>\n\n    <!-- Fade Spread -->\n    <div class="section">', separator)

# Also remove the <br> tags and replace them with separators or just let margins handle it
html = html.replace('<br>', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
