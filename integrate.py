import os

# What we want to inject
HEAD_INJECT = [
    '<link rel="stylesheet" href="custom-cursor.css">',
    '<link rel="stylesheet" href="rightclick.css">'
]

BODY_INJECT = [
    '<script src="custom-cursor.js"></script>',
    '<script src="rightclick.js"></script>'
]

def inject_into_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Inject into <head>
    if "<head>" in content:
        for tag in HEAD_INJECT:
            if tag not in content:
                content = content.replace("<head>", "<head>\n    " + tag)

    # Inject before </body>
    if "</body>" in content:
        for tag in BODY_INJECT:
            if tag not in content:
                content = content.replace("</body>", "    " + tag + "\n</body>")

    # Write only if changed
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")
    else:
        print(f"No changes needed: {filepath}")

def main():
    for file in os.listdir():
        if file.endswith(".html"):
            inject_into_file(file)

if __name__ == "__main__":
    main()
