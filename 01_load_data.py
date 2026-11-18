
import csv

# Load Netflix dataset
with open("dataset/netflix_titles.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    columns = reader.fieldnames
    data = list(reader)

# Display first five records
print("\nFIRST 5 NETFLIX RECORDS")

for record in data[:5]:
    print(record)

# Display dataset shape
print("\nDATASET SHAPE")
print("Rows:", len(data))
print("Columns:", len(columns))

# Display column names
print("\nDATASET COLUMNS")
print(columns)

# Display missing values
print("\nMISSING VALUES")

for column in columns:
    missing = sum(
        1 for record in data
        if not record[column] or not record[column].strip()
    )
    print(column, ":", missing)

print("\nNETFLIX DATASET LOADED SUCCESSFULLY!")

