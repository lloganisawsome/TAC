import os

# Scripts we want to inject
BODY_SCRIPTS = [
    '<script src="custom-cursor.js"></script>',
    '<script src="rightclick.js"></script>',
    '<script src="panic-key.js"></script>',
    '<script src="idle-dvd.js"></script>'
]

# Stylesheets to inject into <head>
HEAD_LINKS = [
    '<link rel="stylesheet" href="custom-cursor.css">',
    '<link rel="stylesheet" href="rightclick.css">'
]

def inject_into_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Inject into <head>
    if "<head>" in content:
        for link in HEAD_LINKS:
            if link not in content:
                content = content.replace("<head>", "<head>\n    " + link)

    # Inject before </body>
    if "</body>" in content:
        for script in BODY_SCRIPTS:
            if script not in content:
                content = content.replace("</body>", "    " + script + "\n</body>")

    # Write only if changed
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")
    else:
        print(f"No changes needed: {filepath}")

def scan_folder(folder="."):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".html"):
                inject_into_file(os.path.join(root, file))

if __name__ == "__main__":
    scan_folder()
