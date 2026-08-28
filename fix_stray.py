import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the specific block that has the extra </div>
old_block = """                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'custom')">Custom Sequence</button>
                </div>
            </div>
        </div>

    </div>
    
        <div class="section" id="customSeqPanel\""""

new_block = """                    <button class="tv-effect-btn" style="margin-top:0;" onclick="setTvEffect(this, 'custom')">Custom Sequence</button>
                </div>
            </div>
        </div>
        
        <div class="section" id="customSeqPanel\""""

html = html.replace(old_block, new_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
