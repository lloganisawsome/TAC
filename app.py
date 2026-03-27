import os
from bs4 import BeautifulSoup

def inject_script_tag(root_dir, script_src):
    tag_to_add = f'<script src="{script_src}"></script>'
    
    # Walk through the directory and subfolders
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if the script is already there to avoid duplicates
                if script_src in content:
                    print(f"Skipping (already present): {file_path}")
                    continue

                soup = BeautifulSoup(content, 'html.parser')
                new_tag = soup.new_tag("script", src=script_src)

                # Try to append to <head>, otherwise <body>, otherwise just at the end
                if soup.head:
                    soup.head.append(new_tag)
                elif soup.body:
                    soup.body.append(new_tag)
                else:
                    soup.append(new_tag)

                # Save the modified file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup.prettify()))
                
                print(f"Successfully updated: {file_path}")

if __name__ == "__main__":
    # Target the current directory
    current_directory = os.getcwd()
    target_script = "app-presence.js"
    
    inject_script_tag(current_directory, target_script)
