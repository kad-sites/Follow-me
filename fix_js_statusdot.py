import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("statusDot.classList.add('connected');", "if(statusDot) statusDot.classList.add('connected');")
js = js.replace("statusDot.classList.remove('connected');", "if(statusDot) statusDot.classList.remove('connected');")

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
