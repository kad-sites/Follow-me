with open('main.js', 'r') as f:
    js = f.read()

js = js.replace('gb(,,);', '\gb(\,\,\)\;', 1)
js = js.replace('gb(,,);', '\gb(\,\,\)\;', 1)

with open('main.js', 'w') as f:
    f.write(js)
