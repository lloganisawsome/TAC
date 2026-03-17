import os

WIDGET_LOADER = """
<div id="tac-phone-container"></div>
<script>
    fetch('phone-widget.html')
        .then(r => r.text())
        .then(html => document.getElementById('tac-phone-container').innerHTML = html);
</script>
"""

def run_injector():
    for file in os.listdir('.'):
        if file.endswith('.html') and file != 'phone-widget.html':
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Prevent double injection
            if any("TAC WIDGET LOADER" in line for line in lines):
                print(f"Skipping {file} (Already Injected)")
                continue

            # Insert before the closing body tag
            for i, line in enumerate(lines):
                if "</body>" in line:
                    lines[i] = line.replace("</body>", f"{WIDGET_LOADER}\n</body>")
                    break
            
            with open(file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Successfully injected into {file}")

if __name__ == "__main__":
    run_injector()
