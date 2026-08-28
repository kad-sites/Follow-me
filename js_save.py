with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add logic to show/hide the save button
old_switch = "if (target) {\n                target.classList.add('active');\n                target.style.display = 'block';\n            }"
new_switch = "if (target) {\n                target.classList.add('active');\n                target.style.display = 'block';\n                \n                const saveBtn = document.getElementById('saveBtnContainer');\n                if(saveBtn) {\n                    saveBtn.style.display = (tabId === 'tv') ? 'block' : 'none';\n                }\n            }"
js = js.replace(old_switch, new_switch)

# Add saveTvSettings function
save_func = """
        window.saveTvSettings = function() {
            if (!isConnected) {
                showToast("Not Connected to Cloud!");
                return;
            }
            const payload = {
                save: true
            };
            client.publish("kad/tvbacklit/cmd/zoheb", JSON.stringify(payload));
            showToast("Settings Saved to Device Memory!");
        };
"""
js = js + "\n" + save_func

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)
