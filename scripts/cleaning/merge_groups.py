import pandas as pd
from pathlib import Path

# ==========================================
# File Paths
# ==========================================

RAW_FOLDER = Path("data/raw/wikipedia")
OUTPUT_FOLDER = Path("data/processed")

# Create output folder if it doesn't exist
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# ==========================================
# Groups
# ==========================================

groups = "ABCDEFGHIJKL"

# List to store all group DataFrames
all_groups = []

# ==========================================
# Read and Process Each Group
# ==========================================

for group in groups:

    file_path = RAW_FOLDER / f"group_{group.lower()}.csv"

    # Check if file exists
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        continue

    print(f"📂 Reading {file_path.name}...")

    # Read CSV
    df = pd.read_csv(file_path)

    # Rename column if present
    if "Teamvte" in df.columns:
        df.rename(
            columns={"Teamvte": "Team"},
            inplace=True
        )

    # Add Group column
    df["Group"] = group

    # Store DataFrame
    all_groups.append(df)

# ==========================================
# Merge All Groups
# ==========================================

if len(all_groups) == 0:
    print("❌ No group files were loaded.")
    exit()

group_standings = pd.concat(
    all_groups,
    ignore_index=True
)

# ==========================================
# Reorder Columns
# ==========================================

columns_order = [
    "Group",
    "Pos",
    "Team",
    "Pld",
    "W",
    "D",
    "L",
    "GF",
    "GA",
    "GD",
    "Pts",
    "Qualification"
]

existing_columns = [
    col for col in columns_order
    if col in group_standings.columns
]

remaining_columns = [
    col for col in group_standings.columns
    if col not in existing_columns
]

group_standings = group_standings[
    existing_columns + remaining_columns
]

# ==========================================
# Save Processed File
# ==========================================

output_file = OUTPUT_FOLDER / "group_standings.csv"

group_standings.to_csv(
    output_file,
    index=False
)

# ==========================================
# Summary
# ==========================================

print("\n===================================")
print("✅ Group Standings Merged Successfully!")
print("===================================")
print(f"📄 Output File : {output_file}")
print(f"📊 Total Rows  : {len(group_standings)}")
print(f"📋 Total Columns : {len(group_standings.columns)}")
print("===================================")