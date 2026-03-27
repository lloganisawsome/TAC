import os

# Text to remove if it exists from previous attempts
BAD_TEXT = "How to embed popup.html on every page"

# Clean Iframe to add
WIDGET_IFRAME = """
<iframe src="popup.html" 
        sandbox="allow-scripts allow-same-origin"
        style="position:fixed; bottom:16px; left:16px; width:340px; height:200px; border:none; overflow:hidden; z-index:9999; background:transparent;" 
        allowtransparency="true">
</iframe>
"""

def process_files():
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'popup.html']
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. REMOVE BAD TEXT (If it's there)
        if BAD_TEXT in content:
            print(f"Cleaning up {filename}...")
            # We split by the bad text and take the first part to revert the file
            content = content.split(BAD_TEXT)[0] 
        
        # 2. INJECT IFRAME (Only if not already there)
        if 'src="popup.html"' not in content:
            if '</body>' in content:
                print(f"Injecting widget into {filename}...")
                content = content.replace('</body>', f'{WIDGET_IFRAME}\n</body>')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                print(f"Skipping {filename}: No </body> tag found.")
        else:
            print(f"Widget already present in {filename}.")

if __name__ == "__main__":
    process_files()
    print("All tasks complete!")
