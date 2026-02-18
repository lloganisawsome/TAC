import os

# The script tag to inject
guard_tag = '<script src="guard.js"></script>'

# Get all HTML files in the current directory
for filename in os.listdir("."):
    if filename.endswith(".html"):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip files that already include the script
        if guard_tag in content:
            print(f"{filename} already has guard.js included, skipping.")
            continue

        # Insert the script after <head> if it exists, otherwise at the top
        if "<head>" in content:
            content = content.replace("<head>", "<head>\n" + guard_tag)
        else:
            content = guard_tag + "\n" + content

        # Save changes
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Injected guard.js script tag into {filename}")
