import os

BODY_INJECT = [
    '<script src="panic-key.js"></script>'
]

def inject_into_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

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
