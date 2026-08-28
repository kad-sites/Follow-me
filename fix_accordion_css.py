import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add CSS for panel-content
css_addition = """
        .panel-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .panel-content.open {
            max-height: 500px; /* Big enough for content */
        }
"""
html = html.replace("</style>", css_addition + "</style>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
