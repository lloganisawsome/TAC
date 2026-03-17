import os

folder = os.path.dirname(os.path.abspath(__file__))

for file in os.listdir(folder):
    if file.endswith(".html"):
        path = os.path.join(folder, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content.replace("href__", "href")

        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {file}")
        else:
            print(f"No change: {file}")
