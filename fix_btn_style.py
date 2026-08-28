with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

css = """
        .tv-effect-btn {
            background: rgba(255,255,255,0.05);
            color: var(--subtext);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 12px;
            width: 100%;
            text-align: left;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 0 !important;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .tv-effect-btn:active {
            transform: scale(0.98);
        }
        .tv-effect-btn.active {
            background: rgba(96, 165, 250, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(96, 165, 250, 0.3);
        }
        .tv-effect-btn.active::after {
            content: '?';
            font-weight: bold;
        }
"""

html = html.replace('</style>', css + '\n</style>')

# Remove action-btn class to let tv-effect-btn take over completely
html = html.replace('class="action-btn tv-effect-btn', 'class="tv-effect-btn')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
