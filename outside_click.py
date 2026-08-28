with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

outside_click_code = """
document.addEventListener('click', function(event) {
    const colorPanel = document.getElementById('tvColorContent') ? document.getElementById('tvColorContent').closest('.dropdown-panel') : null;
    const effectPanel = document.getElementById('tvEffectContent') ? document.getElementById('tvEffectContent').closest('.dropdown-panel') : null;
    
    if (colorPanel && !colorPanel.contains(event.target)) {
        const content = document.getElementById('tvColorContent');
        if (content.classList.contains('open')) {
            content.classList.remove('open');
            document.getElementById('tvColorChevron').style.transform = 'rotate(0deg)';
        }
    }
    
    if (effectPanel && !effectPanel.contains(event.target)) {
        const content = document.getElementById('tvEffectContent');
        if (content.classList.contains('open')) {
            content.classList.remove('open');
            document.getElementById('tvEffectChevron').style.transform = 'rotate(0deg)';
        }
    }
});
"""

js += "\n" + outside_click_code

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
