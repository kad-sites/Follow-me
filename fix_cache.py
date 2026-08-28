with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add aggressive no-cache meta tags right after <head>
cache_bust = """<head>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <script>
    // Force unregister any service workers
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(function(registrations) {
            for (let registration of registrations) {
                registration.unregister();
            }
        });
        // Clear all caches
        if ('caches' in window) {
            caches.keys().then(function(names) {
                for (let name of names) caches.delete(name);
            });
        }
    }
    </script>"""

html = html.replace("<head>", cache_bust)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
