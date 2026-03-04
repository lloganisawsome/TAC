import os
import re

SCRIPT_TAG = '<script src="online.js"></script>\n'

def inject_script_into_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if script already exists
    if "online.js" in content:
        print(f"[SKIPPED] {file_path} (already contains online.js)")
        return

    # Insert before </body> if it exists
    if re.search(r"</body>", content, re.IGNORECASE):
        content = re.sub(
            r"</body>",
            SCRIPT_TAG + "</body>",
            content,
            flags=re.IGNORECASE
        )
    else:
        # If no </body>, append at end
        content += "\n" + SCRIPT_TAG

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[UPDATED] {file_path}")

def process_directory(directory="."):
    for filename in os.listdir(directory):
        if filename.lower().endswith(".html"):
            file_path = os.path.join(directory, filename)
            inject_script_into_html(file_path)

if __name__ == "__main__":
    process_directory()
