import os
import glob

# The script tag linking to the external file
SCRIPT_TAG = '<script src="emojis.js"></script>'

def inject_emoji_link():
    # Find all .html files in the current directory only
    html_files = glob.glob("*.html")
    
    if not html_files:
        print("No HTML files found in this directory.")
        return

    for file_path in html_files:
        # Skip the file if it somehow reads itself
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if the tag is already there
        if SCRIPT_TAG in content:
            print(f"Skipping '{file_path}' (Link already exists)")
            continue
            
        # Insert the script tag right before the closing body tag
        if "</body>" in content:
            updated_content = content.replace("</body>", SCRIPT_TAG + "\n</body>")
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Successfully linked: {file_path}")
        else:
            print(f"Skipped '{file_path}' (Could not find a </body> tag)")

if __name__ == "__main__":
    inject_emoji_link()
