import pandas as pd
from pathlib import Path

# ==========================================
# STAGE 3.1 — PROCESS FLOW ANALYSIS
# ==========================================

INPUT_FILE = Path("data/processed/procurement_timing_features.csv")

print("Loading processed procurement data...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df)}")
print(f"Columns available: {len(df.columns)}")

print("\n========================================")
print("DATASET COLUMNS")
print("========================================")

for column in df.columns:
    print(column)

# ==========================================
# IDENTIFY CASE AND ACTIVITY COLUMNS
# ==========================================

case_candidates = [
    "case_id",
    "case",
    "Case ID",
    "caseid"
]

case_column = None

for column in case_candidates:
    if column in df.columns:
        case_column = column
        break

if case_column is None:
    print("\nWARNING: Case ID column not automatically detected.")
else:
    print(f"\nCase ID column: {case_column}")

# ==========================================
# BASIC PROCESS STATISTICS
# ==========================================

print("\n========================================")
print("PROCESS STATISTICS")
print("========================================")

if case_column:
    print(f"Unique procurement cases: {df[case_column].nunique()}")

print(f"Total rows: {len(df)}")

# ==========================================
# NUMERIC FEATURE SUMMARY
# ==========================================

numeric_columns = df.select_dtypes(include="number").columns

print("\n========================================")
print("NUMERIC PROCESS FEATURES")
print("========================================")

if len(numeric_columns) > 0:
    summary = df[numeric_columns].describe().T

    print(summary[
        ["count", "mean", "min", "50%", "max"]
    ].round(2))

else:
    print("No numeric features found.")

# ==========================================
# SAVE INITIAL PROCESS ANALYSIS
# ==========================================

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "procurement_process_analysis.csv"

df.to_csv(OUTPUT_FILE, index=False)

print("\n========================================")
print("STAGE 3.1 COMPLETED")
print("========================================")

print(f"Output file: {OUTPUT_FILE}")