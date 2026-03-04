import os
import re

MODULE_TAG = '<script type="module" src="online.js"></script>\n'

def fix_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # 1️⃣ Remove ANY script tag that references online.js
    content = re.sub(
        r'<script[^>]*src=["\']online\.js["\'][^>]*>\s*</script>',
        '',
        content,
        flags=re.IGNORECASE
    )

    # 2️⃣ Check if module tag already exists
    if MODULE_TAG.strip() in content:
        print(f"[OK] {file_path} already correct")
        return

    # 3️⃣ Insert before </body> if present
    if re.search(r"</body>", content, re.IGNORECASE):
        content = re.sub(
            r"</body>",
            MODULE_TAG + "</body>",
            content,
            flags=re.IGNORECASE
        )
    else:
        # If no </body>, append to end
        content += "\n" + MODULE_TAG

    # 4️⃣ Save only if changed
    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[UPDATED] {file_path}")
    else:
        print(f"[SKIPPED] {file_path}")

def process_directory(directory="."):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(".html"):
                file_path = os.path.join(root, filename)
                fix_html_file(file_path)

if __name__ == "__main__":
    process_directory()
