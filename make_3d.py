import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_css = """        .color-swatch {
            width: 32px; /* Smaller swatches */
            height: 32px;
            border-radius: 50%;
            box-shadow: 0 2px 6px rgba(0,0,0,0.4);
            border: 2px solid transparent;
            transition: all 0.2s;
        }"""

new_css = """        .color-swatch {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            /* 3D Drop Shadow + Inner Highlights */
            box-shadow: 
                0 4px 6px rgba(0,0,0,0.6), 
                inset 0 3px 5px rgba(255,255,255,0.5), 
                inset 0 -4px 6px rgba(0,0,0,0.5);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        /* Satin specular finish overlay */
        .color-swatch::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 40%, rgba(0,0,0,0.1) 100%);
            border-radius: 50%;
            pointer-events: none;
        }"""

html = html.replace(old_css, new_css)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
