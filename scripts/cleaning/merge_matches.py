import pandas as pd
from pathlib import Path

# ==========================================
# File Paths
# ==========================================

RAW_FOLDER = Path("data/raw/wikipedia")
OUTPUT_FOLDER = Path("data/processed")

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# ==========================================
# Groups
# ==========================================

groups = "ABCDEFGHIJKL"

all_matches = []

# ==========================================
# Read Match Files
# ==========================================

for group in groups:

    file_path = RAW_FOLDER / f"group_{group.lower()}_matches.csv"

    if not file_path.exists():
        print(f"❌ Missing: {file_path}")
        continue

    print(f"📂 Reading {file_path.name}")

    df = pd.read_csv(file_path)

    # Add Group
    df["Group"] = group

    all_matches.append(df)

# ==========================================
# Merge
# ==========================================

if len(all_matches) == 0:
    print("❌ No match files found.")
    exit()

matches = pd.concat(
    all_matches,
    ignore_index=True
)

# ==========================================
# Save
# ==========================================

output_file = OUTPUT_FOLDER / "matches.csv"

matches.to_csv(
    output_file,
    index=False
)

print("\n===================================")
print("✅ Match Schedule Merged Successfully!")
print("===================================")
print(f"📄 Output : {output_file}")
print(f"📊 Rows   : {len(matches)}")
print(f"📋 Columns: {len(matches.columns)}")
print("===================================")