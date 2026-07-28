from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw/world_cup_2026")

for csv_file in RAW_DIR.glob("*.csv"):
    print("=" * 60)
    print(f"File: {csv_file.name}")

    df = pd.read_csv(csv_file)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())