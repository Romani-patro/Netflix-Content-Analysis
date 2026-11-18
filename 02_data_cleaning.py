
import csv
from datetime import datetime

# STEP 1: Load the original Netflix dataset

input_file = "dataset/netflix_titles.csv"
output_file = "dataset/netflix_cleaned.csv"

with open(input_file, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    data = list(reader)
    columns = reader.fieldnames

print("Original records:", len(data))


# STEP 2: Remove duplicate records using show_id

unique_data = []
seen_ids = set()

for row in data:
    show_id = row["show_id"].strip()

    if show_id not in seen_ids:
        seen_ids.add(show_id)
        unique_data.append(row)

print("Duplicate records removed:", len(data) - len(unique_data))


# STEP 3: Remove unnecessary spaces

for row in unique_data:
    for column in columns:
        if row[column]:
            row[column] = row[column].strip()


# STEP 4: Handle missing values

missing_columns = [
    "director",
    "cast",
    "country",
    "rating",
    "duration",
    "listed_in"
]

for row in unique_data:
    for column in missing_columns:
        if not row[column]:
            row[column] = "Unknown"


# STEP 5: Convert date_added into YYYY-MM-DD format

for row in unique_data:
    date_value = row["date_added"]

    if date_value:
        try:
            date_object = datetime.strptime(
                date_value, "%B %d, %Y"
            )
            row["date_added"] = date_object.strftime("%Y-%m-%d")

        except ValueError:
            print("Could not convert date:", date_value)


# STEP 6: Save the cleaned dataset

with open(output_file, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(unique_data)


# STEP 7: Display cleaning summary

print("\n========== DATA CLEANING SUMMARY ==========")

print("Original records:", len(data))
print("Cleaned records:", len(unique_data))
print("Duplicate records removed:", len(data) - len(unique_data))

print("\nCleaned dataset saved successfully!")
print("File location:", output_file)
