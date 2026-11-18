
import csv
from collections import Counter

# Load cleaned Netflix dataset

with open("dataset/netflix_cleaned.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    data = list(reader)

print("NETFLIX EXPLORATORY DATA ANALYSIS")
print("=" * 45)


# 1. Movies vs TV Shows

content_types = Counter(row["type"] for row in data)

print("\n1. MOVIES VS TV SHOWS")

for content, count in content_types.items():
    print(content, ":", count)


# 2. Top 10 Countries

countries = Counter()

for row in data:
    if row["country"] != "Unknown":
        for country in row["country"].split(","):
            countries[country.strip()] += 1

print("\n2. TOP 10 COUNTRIES")

for country, count in countries.most_common(10):
    print(country, ":", count)


# 3. Content released by year

release_years = Counter()

for row in data:
    if row["release_year"]:
        release_years[row["release_year"]] += 1

print("\n3. TOP 10 RELEASE YEARS")

for year, count in release_years.most_common(10):
    print(year, ":", count)


# 4. Top 10 Genres

genres = Counter()

for row in data:
    if row["listed_in"] != "Unknown":
        for genre in row["listed_in"].split(","):
            genres[genre.strip()] += 1

print("\n4. TOP 10 GENRES")

for genre, count in genres.most_common(10):
    print(genre, ":", count)


# 5. Movies and TV Shows added each year

added_years = Counter()

for row in data:
    date_added = row["date_added"]

    if date_added and date_added != "Unknown":
        year = date_added[:4]
        added_years[year] += 1

print("\n5. CONTENT ADDED BY YEAR")

for year, count in sorted(added_years.items()):
    print(year, ":", count)


print("\nEDA COMPLETED SUCCESSFULLY!")
