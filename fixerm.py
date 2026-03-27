import os

# The exact text that was accidentally injected
TEXT_TO_REMOVE = """How to embed popup.html on every page
Add this snippet to the <body> of any page you want the widget on (exactly like your existing phone-widget.html pattern):"""

def cleanup_files():
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        if TEXT_TO_REMOVE in content:
            print(f"Cleaning up {filename}...")
            # Replace the accidental text with nothing
            new_content = content.replace(TEXT_TO_REMOVE, "")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
        else:
            print(f"No mess found in {filename}.")

if __name__ == "__main__":
    cleanup_files()
    print("Cleanup complete!")
