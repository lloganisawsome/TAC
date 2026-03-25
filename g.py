import csv
import os
import re

# Name of the text file containing filenames
txt_file = "filenames.txt"  # <-- put your file list here

# Check if the file exists
if not os.path.exists(txt_file):
    print(f"Error: {txt_file} not found in the current directory.")
    exit()

# Read all lines from the text file
with open(txt_file, "r") as f:
    file_names = [line.strip() for line in f if line.strip()]

# CSV output file
output_csv = "output.csv"

with open(output_csv, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["title", "iframe", "imageurl"])
    writer.writeheader()

    for name in file_names:
        # Remove extension (.html or .htm)
        if name.lower().endswith(".html"):
            title = name[:-5]  # remove .html
        elif name.lower().endswith(".htm"):
            title = name[:-4]  # remove .htm
        else:
            title = name

        # Remove 'c' and 'l' from title
        title = title.replace('c', '').replace('l', '')

        # Add a space before each capital letter (except the first character)
        title = re.sub(r'(?<!^)([A-Z])', r' \1', title)

        # Build iframe URL
        iframe = f"https://raw.githubusercontent.com/bubbls/ugs-singlefile/refs/heads/main/UGS-Files/{name}"
        imageurl = "blank.png"

        writer.writerow({
            "title": title,
            "iframe": iframe,
            "imageurl": imageurl
        })

print(f"CSV generated: {output_csv}")
