import re

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Fix the syntax error
bad_code = """                      if (tvEffect === 'custom') {
                          document.getElementById('customSeqPanel').style.display = 'block';
                      } else {
                          document.getElementById('customSeqPanel').style.display = 'none';
                      }
                  });
                    }"""
good_code = """                      if (tvEffect === 'custom') {
                          document.getElementById('customSeqPanel').style.display = 'block';
                      } else {
                          document.getElementById('customSeqPanel').style.display = 'none';
                      }
                  }"""

js = js.replace(bad_code, good_code)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
