# inject_time_tracker.py
import os

# Name of the JS file
js_filename = "timeTracker.js"

# Loop through all HTML files in the current directory
for file in os.listdir("."):
    if file.endswith(".html"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if the script is already injected
        if js_filename in content:
            print(f"Skipped {file}, already contains {js_filename}")
            continue
        
        # Inject the script before </body>
        if "</body>" in content:
            content = content.replace("</body>", f'    <script src="{js_filename}"></script>\n</body>')
        else:
            # If no </body>, just append at the end
            content += f'\n<script src="{js_filename}"></script>\n'
        
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Injected {js_filename} into {file}")

print("Done injecting into all HTML files.")
