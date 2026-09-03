with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Add the new text effects
new_effects = """
                        <div style="height: 1px; background: rgba(255,255,255,0.05); margin: 6px 0;"></div>
                        <span style="font-size: 11px; color: var(--subtext); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; padding-left: 8px;">Text Animations</span>
                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, 'text_fade')">Text: Soft Fade</button>
                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, 'text_drop')">Text: Drop Build</button>
                        <button class="tv-effect-btn px-effect-btn" style="margin-top:0;" onclick="setPxEffect(this, 'text_slide')">Text: Slide Left</button>"""

html = re.sub(r'(<button class="[^"]+"[^>]*onclick="setPxEffect\(this,\s*\'fire\'\)">[^<]+</button>)', r'\1' + new_effects, html)

# Add the text input section
text_section = """
            <div class="section" style="margin-bottom: 8px;">
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 14px; font-weight: 500;">Matrix Text</span>
                        <span style="font-size: 12px; color: var(--subtext);">For text animations</span>
                    </div>
                    <input type="text" id="pxTextInput" placeholder="e.g. ZOHEB" style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: white; padding: 10px 12px; font-size: 14px; box-sizing: border-box; outline: none; transition: border-color 0.2s;" onfocus="this.style.borderColor='rgba(96, 165, 250, 0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
                </div>
            </div>"""

html = re.sub(r'(<div class="section dropdown-panel" id="pxEffectPanel">)', text_section + r'\n            \1', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
