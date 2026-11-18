
import csv
import mysql.connector
from pathlib import Path
from datetime import datetime
from getpass import getpass

# Find the project folder and CSV file
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_FOLDER / "dataset" / "netflix_cleaned.csv"

# Read the CSV file
with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print("Total CSV records:", len(rows))

if len(rows) != 8807:
    raise ValueError("Expected 8807 records. Please check your CSV file.")

# Connect to MySQL
password = getpass("Enter your MySQL root password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="netflix_analysis",
    port=3306
)

cursor = connection.cursor()

# Prepare the SQL query
sql = """
INSERT INTO netflix (
    show_id, type, title, director, cast, country,
    date_added, release_year, rating, duration,
    listed_in, description
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = []

for row in rows:
    date_value = row["date_added"].strip()

    if date_value:
        date_value = datetime.strptime(
            date_value, "%Y-%m-%d"
        ).date()
    else:
        date_value = None

    release_year = row["release_year"].strip()

    if release_year:
        release_year = int(release_year)
    else:
        release_year = None

    data.append((
        row["show_id"],
        row["type"],
        row["title"],
        row["director"],
        row["cast"],
        row["country"],
        date_value,
        release_year,
        row["rating"],
        row["duration"],
        row["listed_in"],
        row["description"]
    ))

try:
    # Replace previous incomplete imports
    cursor.execute("DELETE FROM netflix")

    # Insert all CSV records
    cursor.executemany(sql, data)

    connection.commit()

    print("\nDATA IMPORTED SUCCESSFULLY!")

    cursor.execute("SELECT COUNT(*) FROM netflix")
    total = cursor.fetchone()[0]

    print("Total records in MySQL:", total)

except Exception as error:
    connection.rollback()
    print("IMPORT FAILED:", error)

finally:
    cursor.close()
    connection.close()
