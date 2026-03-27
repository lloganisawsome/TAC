import os
import csv

folder = os.getcwd()
output_csv = "songs.csv"

songs_data = []

for filename in os.listdir(folder):
    if filename.lower().endswith(".mp3"):
        original_path = os.path.join(folder, filename)

        # Remove ES_ from filename
        new_filename = filename.replace("ES_", "")
        new_path = os.path.join(folder, new_filename)

        # Rename file if needed
        if filename != new_filename:
            os.rename(original_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

        # Clean name (remove .mp3)
        name = new_filename.replace(".mp3", "")

        # Optional: make it nicer (replace dashes/underscores)
        name_clean = name.replace("-", " ").replace("_", " ")

        # Add to CSV (adjust path if needed)
        songs_data.append([name_clean, f"music/{new_filename}"])

# Write CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "filename"])
    writer.writerows(songs_data)

print(f"\nDone. CSV saved as {output_csv}")
