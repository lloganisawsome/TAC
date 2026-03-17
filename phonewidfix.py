import os

old = """<div id="tac-phone-container"></div>
<script>
    fetch('phone-widget.html')
        .then(r => r.text())
        .then(html => document.getElementById('tac-phone-container').innerHTML = html);
</script>"""

new = """<div id="tac-phone-container"></div>
<script>
    fetch('phone-widget.html')
        .then(r => r.text())
        .then(html => {
            const container = document.getElementById('tac-phone-container');
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');"""

folder = os.path.dirname(os.path.abspath(__file__))

for file in os.listdir(folder):
    if file.endswith(".html"):
        path = os.path.join(folder, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if old in content:
            content = content.replace(old, new)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Replaced in {file}")
        else:
            print(f"Skipped {file} (not found)")
