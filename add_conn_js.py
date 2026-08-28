import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

connect_old = """        client.on('connect', () => {
            console.log('Connected to MQTT via WebSockets');
            statusDot.classList.add('connected');
            isConnected = true;"""

connect_new = """        client.on('connect', () => {
            console.log('Connected to MQTT via WebSockets');
            statusDot.classList.add('connected');
            document.getElementById('connErrorMsg').style.display = 'none';
            isConnected = true;"""

close_old = """        client.on('close', () => {
            statusDot.classList.remove('connected');
            isConnected = false;
        });"""

close_new = """        client.on('close', () => {
            statusDot.classList.remove('connected');
            document.getElementById('connErrorMsg').style.display = 'block';
            isConnected = false;
        });"""

js = js.replace(connect_old, connect_new)
js = js.replace(close_old, close_new)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)
