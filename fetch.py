import csv
import re
import os

# Name of your RTF file
rtf_file = "filenames.rtf"  # <-- make sure it's in the same folder

if not os.path.exists(rtf_file):
    print(f"Error: {rtf_file} not found in the current directory.")
    exit()

# Read the RTF file as plain text
with open(rtf_file, "r", encoding="utf-8") as f:
    rtf_content = f.read()

# Remove RTF formatting codes
# This is a simple way to strip \word and { } formatting
text_only = re.sub(r'\\[a-z]+\d*', '', rtf_content)  # remove \commands
text_only = re.sub(r'{|}', '', text_only)            # remove braces

# Split lines and remove empty lines
file_names = [line.strip() for line in text_only.splitlines() if line.strip()]

# CSV output file
output_csv = "output.csv"

with open(output_csv, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["title", "iframe", "imageurl"])
    writer.writeheader()

    for name in file_names:
        # Remove extension (.html or .htm)
        if name.lower().endswith(".html"):
            title = name[:-5]
        elif name.lower().endswith(".htm"):
            title = name[:-4]
        else:
            title = name

        # Remove 'c' and 'l' from title
        title = title.replace('c', '').replace('l', '')

        # Build iframe URL
        iframe = f"https://raw.githubusercontent.com/bubbls/ugs-singlefile/refs/heads/main/UGS-Files/{name}"
        imageurl = "blank.png"

        writer.writerow({
            "title": title,
            "iframe": iframe,
            "imageurl": imageurl
        })

print(f"CSV generated: {output_csv}")
