import pandas as pd
from pathlib import Path

# ==========================================================
# FIFA World Cup Analytics
# ETL Pipeline - Clean Qualified Teams
# ==========================================================

RAW_FOLDER = Path("data/raw/wikipedia")
OUTPUT_FOLDER = Path("data/processed")

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_FOLDER / "qualified_teams.csv"
OUTPUT_FILE = OUTPUT_FOLDER / "qualified_teams.csv"

# ==========================================================
# Read Dataset
# ==========================================================

print("📂 Reading qualified_teams.csv...")

df = pd.read_csv(INPUT_FILE)

print(f"✅ Loaded {len(df)} rows")

# ==========================================================
# Remove Duplicate Rows
# ==========================================================

duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)

print(f"🗑 Removed {duplicates} duplicate rows")

# ==========================================================
# Remove Empty Rows
# ==========================================================

df.dropna(how="all", inplace=True)

# ==========================================================
# Trim Spaces
# ==========================================================

text_columns = df.select_dtypes(include="object").columns

for column in text_columns:
    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
    )

# ==========================================================
# Remove Wikipedia Footnotes
# Example:
# Brazil[2]
# Canada[A]
# ==========================================================

for column in text_columns:
    df[column] = df[column].str.replace(
        r"\[.*?\]",
        "",
        regex=True
    )

# ==========================================================
# Remove Host Symbol
#
# Mexico (H)
# Canada (H)
# ==========================================================

if "Team" in df.columns:

    df["Team"] = (
        df["Team"]
        .str.replace(r"\s*\(H\)", "", regex=True)
        .str.strip()
    )

# ==========================================================
# Rename Columns
# ==========================================================

rename_dict = {}

if "Method of qualification" in df.columns:
    rename_dict["Method of qualification"] = "Qualification_Method"

if "Date of qualification" in df.columns:
    rename_dict["Date of qualification"] = "Qualification_Date"

if "Confederation" in df.columns:
    rename_dict["Confederation"] = "Confederation"

df.rename(
    columns=rename_dict,
    inplace=True
)

# ==========================================================
# Sort Teams Alphabetically
# ==========================================================

if "Team" in df.columns:
    df.sort_values(
        by="Team",
        inplace=True
    )

# ==========================================================
# Reset Index
# ==========================================================

df.reset_index(
    drop=True,
    inplace=True
)

# ==========================================================
# Save
# ==========================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ==========================================================
# Summary
# ==========================================================

print("\n========================================")
print("✅ Qualified Teams Cleaned Successfully!")
print("========================================")
print(f"📄 Output : {OUTPUT_FILE}")
print(f"📊 Rows   : {len(df)}")
print(f"📋 Columns: {len(df.columns)}")
print("========================================")