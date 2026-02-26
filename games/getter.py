import os
import csv

# Folder where script lives
folder_path = os.path.dirname(os.path.abspath(__file__))

# Output CSV path
csv_path = os.path.join(folder_path, "games.csv")

rows = []

for file in os.listdir(folder_path):
    if file.endswith(".html"):
        name = os.path.splitext(file)[0]
        iframe_url = f"games/{name}"
        rows.append([name, iframe_url, "blank.png"])

# Write CSV
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Iframe URL", "Logo"])
    writer.writerows(rows)

print("games.csv created successfully.")
