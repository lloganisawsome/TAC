import os

# The snippet to inject
WIDGET_HTML = """
<iframe src="popup.html" 
        style="position:fixed; bottom:16px; left:16px; width:340px; height:200px; border:none; overflow:hidden; z-index:9999; background:transparent;" 
        allowtransparency="true">
</iframe>
"""

def inject_widget():
    # Get all files in the current directory
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    # We don't want to inject the widget into the popup itself!
    if 'popup.html' in files:
        files.remove('popup.html')

    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if it's already injected to prevent duplicates
        if 'src="popup.html"' in content:
            print(f"Skipping {filename}: Widget already exists.")
            continue

        # Find the closing body tag
        if '</body>' in content:
            print(f"Injecting into {filename}...")
            new_content = content.replace('</body>', f'{WIDGET_HTML}\n</body>')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
        else:
            print(f"Skipping {filename}: No </body> tag found.")

if __name__ == "__main__":
    inject_widget()
    print("Done!")
