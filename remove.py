import os

# The exact text block to remove
block_to_remove = """Save that as your developerdashboard.html and it should work correctly now. The 4 bugs are fixed — no other logic was changed. 3 hours ago can u fix it and give me the fuol fixed code NOT A BASE44 APP! 3 hours ago Revert L Base44 AI Base44 I understand — you just want the fixed HTML file. Here are all the bugs I found and the corrected full code: Bugs fixed: Stray tag on line 297 #page-modmanagement div was placed outside"""

# Get all files in the current directory
for filename in os.listdir("."):
    if filename.endswith(".html"):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove the exact block
        new_content = content.replace(block_to_remove, "")

        # Overwrite the file with cleaned content
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Cleaned {filename}")
