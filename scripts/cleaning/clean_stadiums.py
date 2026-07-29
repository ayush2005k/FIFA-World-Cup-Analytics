import pandas as pd
from pathlib import Path

# ==========================================================
# FIFA World Cup Analytics
# ETL Pipeline - Clean Stadium Data
# ==========================================================

# -----------------------------
# File Paths
# -----------------------------
RAW_FOLDER = Path("data/raw/wikipedia")
OUTPUT_FOLDER = Path("data/processed")

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_FOLDER / "stadiums.csv"
OUTPUT_FILE = OUTPUT_FOLDER / "stadiums.csv"

# -----------------------------
# Read Dataset
# -----------------------------
print("📂 Reading stadiums.csv...")

df = pd.read_csv(INPUT_FILE)

print(f"✅ Loaded {len(df)} rows")

# ==========================================================
# Basic Inspection
# ==========================================================

print("\n========== Dataset Information ==========")
print(df.info())

# ==========================================================
# Remove Duplicate Rows
# ==========================================================

duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)

print(f"\n🗑 Removed {duplicates} duplicate rows")

# ==========================================================
# Remove Completely Empty Rows
# ==========================================================

df.dropna(how="all", inplace=True)

# ==========================================================
# Remove Image Column
# ==========================================================

if "Image" in df.columns:
    df.drop(columns=["Image"], inplace=True)

# ==========================================================
# Clean Text Columns
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
# Kansas City[F] -> Kansas City
# ==========================================================

for column in text_columns:
    df[column] = df[column].str.replace(
        r"\[.*?\]",
        "",
        regex=True
    )

# ==========================================================
# Clean Stadium Names
# Example:
# Estadio Azteca (Mexico City Stadium)
# ->
# Estadio Azteca
# ==========================================================

df["Stadium"] = (
    df["Stadium"]
    .str.replace(r"\s*\(.*?\)", "", regex=True)
    .str.strip()
)

# ==========================================================
# Clean Capacity
# Example:
# 80,824 -> 80824
# ==========================================================

df["Capacity"] = (
    df["Capacity"]
    .astype(str)
    .str.replace(",", "", regex=False)
)

df["Capacity"] = pd.to_numeric(
    df["Capacity"],
    errors="coerce"
)

# ==========================================================
# Extract Total Matches
#
# Example:
# 5 (3 group, 2 knockout)
#
# becomes
#
# Matches = 5
# ==========================================================

df["Matches"] = (
    df["Number of matches"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(int)
)

# ==========================================================
# Rename Columns
# ==========================================================

df.rename(
    columns={
        "City[G]": "City",
        "Number of matches": "Match_Details"
    },
    inplace=True
)

# ==========================================================
# Reorder Columns
# ==========================================================

column_order = [
    "City",
    "Stadium",
    "Capacity",
    "Matches",
    "Match_Details"
]

remaining_columns = [
    column for column in df.columns
    if column not in column_order
]

df = df[column_order + remaining_columns]

# ==========================================================
# Save Clean Dataset
# ==========================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ==========================================================
# Summary
# ==========================================================

print("\n========================================")
print("✅ Stadium Cleaning Completed!")
print("========================================")
print(f"📄 Output File : {OUTPUT_FILE}")
print(f"📊 Rows        : {len(df)}")
print(f"📋 Columns     : {len(df.columns)}")
print("========================================")