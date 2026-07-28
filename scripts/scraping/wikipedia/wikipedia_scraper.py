import os
import requests
import pandas as pd
from io import StringIO

# -----------------------------
# Create output folder
# -----------------------------
output_folder = "data/raw/wikipedia"
os.makedirs(output_folder, exist_ok=True)

# -----------------------------
# Download Wikipedia page
# -----------------------------
url = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

# -----------------------------
# Read all HTML tables
# -----------------------------
tables = pd.read_html(StringIO(response.text))

print(f"Total tables found: {len(tables)}")

# -----------------------------
# Save Stadiums
# -----------------------------
tables[5].to_csv(
    f"{output_folder}/stadiums.csv",
    index=False
)
print("✓ stadiums.csv saved")

# -----------------------------
# Save Qualified Teams
# -----------------------------
tables[6].to_csv(
    f"{output_folder}/qualified_teams.csv",
    index=False
)
print("✓ qualified_teams.csv saved")

# -----------------------------
# Save Group Standings (A-L)
# -----------------------------
groups = "ABCDEFGHIJKL"

table_index = 9

for group in groups:
    tables[table_index].to_csv(
        f"{output_folder}/group_{group.lower()}.csv",
        index=False
    )

    print(f"✓ group_{group.lower()}.csv saved")

    table_index += 2

# -----------------------------
# Save Group Matches (A-L)
# -----------------------------
table_index = 10

for group in groups:
    tables[table_index].to_csv(
        f"{output_folder}/group_{group.lower()}_matches.csv",
        index=False
    )

    print(f"✓ group_{group.lower()}_matches.csv saved")

    table_index += 2

# -----------------------------
# Save Best Third-Placed Teams
# -----------------------------
tables[33].to_csv(
    f"{output_folder}/best_third_placed_teams.csv",
    index=False
)
print("✓ best_third_placed_teams.csv saved")

# -----------------------------
# Save Knockout Bracket
# -----------------------------
tables[34].to_csv(
    f"{output_folder}/knockout_bracket.csv",
    index=False
)
print("✓ knockout_bracket.csv saved")

# -----------------------------
# Save Tournament Standings
# -----------------------------
tables[68].to_csv(
    f"{output_folder}/tournament_standings.csv",
    index=False
)
print("✓ tournament_standings.csv saved")

print("\n🎉 All useful Wikipedia datasets have been saved successfully!")