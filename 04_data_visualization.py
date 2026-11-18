
import csv
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

# ==========================================
# NETFLIX DATA VISUALIZATION
# THEME: EMERALD DARK
# ==========================================

# Create screenshots folder
Path("screenshots").mkdir(exist_ok=True)

# Load cleaned Netflix dataset
with open("dataset/netflix_cleaned.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    data = list(reader)

print("Dataset loaded successfully:", len(data), "records")


# ==========================================
# EMERALD DARK THEME SETTINGS
# ==========================================

BACKGROUND = "#10251F"
PLOT_BACKGROUND = "#18382D"
EMERALD = "#10B981"
MINT = "#6EE7B7"
WHITE = "#FFFFFF"
GRID = "#355548"

def apply_theme(title, xlabel, ylabel):
    """Apply consistent Emerald Dark styling."""

    fig, ax = plt.subplots(figsize=(10, 6))

    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(PLOT_BACKGROUND)

    ax.set_title(
        title,
        color=WHITE,
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    ax.set_xlabel(xlabel, color=MINT, fontsize=11)
    ax.set_ylabel(ylabel, color=MINT, fontsize=11)

    ax.tick_params(colors=WHITE)

    ax.grid(
        axis="y",
        color=GRID,
        linestyle="--",
        alpha=0.7
    )

    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color(GRID)

    return fig, ax


def add_bar_labels(ax, bars):
    """Display numerical values on bars."""

    for bar in bars:
        height = bar.get_height()

        ax.annotate(
            f"{int(height):,}",
            (bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            color=WHITE,
            fontsize=10,
            fontweight="bold"
        )


def save_chart(fig, filename):
    """Save chart with dark background."""

    fig.tight_layout()

    fig.savefig(
        f"screenshots/{filename}",
        dpi=300,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight"
    )

    plt.close(fig)

    print(filename, "saved successfully!")


# ==========================================
# GRAPH 1: MOVIES VS TV SHOWS
# ==========================================

content_types = Counter(row["type"] for row in data)

fig, ax = apply_theme(
    "Netflix Movies vs TV Shows",
    "Content Type",
    "Number of Titles"
)

bars = ax.bar(
    content_types.keys(),
    content_types.values(),
    color=[EMERALD, MINT],
    width=0.5
)

add_bar_labels(ax, bars)

save_chart(fig, "01_content_types.png")


# ==========================================
# GRAPH 2: TOP 10 COUNTRIES
# ==========================================

countries = Counter()

for row in data:
    if row["country"] != "Unknown":
        for country in row["country"].split(","):
            countries[country.strip()] += 1

top_countries = countries.most_common(10)

fig, ax = apply_theme(
    "Top 10 Netflix Content-Producing Countries",
    "Number of Titles",
    "Country"
)

country_names = [item[0] for item in reversed(top_countries)]
country_counts = [item[1] for item in reversed(top_countries)]

bars = ax.barh(
    country_names,
    country_counts,
    color=EMERALD
)

for bar in bars:
    width = bar.get_width()

    ax.annotate(
        f"{int(width):,}",
        (width, bar.get_y() + bar.get_height() / 2),
        xytext=(6, 0),
        textcoords="offset points",
        va="center",
        color=WHITE,
        fontsize=9,
        fontweight="bold"
    )

save_chart(fig, "02_top_countries.png")


# ==========================================
# GRAPH 3: CONTENT BY RELEASE YEAR
# ==========================================

release_years = Counter(
    row["release_year"]
    for row in data
    if row["release_year"]
)

years = sorted(release_years.keys(), key=int)
counts = [release_years[year] for year in years]

fig, ax = apply_theme(
    "Netflix Content by Release Year",
    "Release Year",
    "Number of Titles"
)

ax.plot(
    years,
    counts,
    color=MINT,
    marker="o",
    markersize=5,
    linewidth=2
)

ax.fill_between(
    years,
    counts,
    color=EMERALD,
    alpha=0.2
)

# Label the five highest release years
top_release_years = sorted(
    release_years.items(),
    key=lambda item: item[1],
    reverse=True
)[:5]

for year, count in top_release_years:
    ax.annotate(
        f"{count:,}",
        (year, count),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        color=WHITE,
        fontsize=9,
        fontweight="bold"
    )

ax.tick_params(axis="x", rotation=45)

save_chart(fig, "03_release_years.png")


# ==========================================
# GRAPH 4: CONTENT ADDED BY YEAR
# ==========================================

added_years = Counter()

for row in data:
    date_added = row["date_added"]

    if date_added and date_added != "Unknown":
        added_years[date_added[:4]] += 1

sorted_years = sorted(added_years.items())

fig, ax = apply_theme(
    "Netflix Content Added by Year",
    "Year",
    "Number of Titles"
)

year_names = [item[0] for item in sorted_years]
year_counts = [item[1] for item in sorted_years]

bars = ax.bar(
    year_names,
    year_counts,
    color=EMERALD,
    width=0.65
)

add_bar_labels(ax, bars)

ax.tick_params(axis="x", rotation=45)

save_chart(fig, "04_content_added_year.png")


# ==========================================
# FINAL STATUS
# ==========================================

print("\n" + "=" * 45)
print("ALL FOUR GRAPHS CREATED SUCCESSFULLY!")
print("Theme: Emerald Dark")
print("Numerical labels: Enabled")
print("Location: screenshots folder")
print("=" * 45)
