with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

old_func = r"""            function setPxEffect\(btn, effect\) \{
                document\.querySelectorAll\('\.px-effect-btn'\)\.forEach\(b => \{
                    b\.classList\.remove\('active'\);
                    b\.innerHTML = b\.innerHTML\.replace\(' <span style="float:right">\?</span>', ''\);
                \}\);
                btn\.classList\.add\('active'\);
                btn\.innerHTML \+= ' <span style="float:right">\?</span>';
                pxEffect = effect;
                sendPxUpdate\(\);
            \}"""

new_func = """            function setPxEffect(btn, effect) {
                document.querySelectorAll('.px-effect-btn').forEach(b => {
                    b.classList.remove('active');
                });
                btn.classList.add('active');
                pxEffect = effect;
                sendPxUpdate();
            }"""

js = re.sub(old_func, new_func, js)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
