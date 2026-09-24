import pandas as pd
import os

# ============================================================
# STAGE 4.1 — DELAY TARGET CREATION
# ============================================================

INPUT_FILE = "data/processed/procurement_process_analysis.csv"
OUTPUT_FILE = "data/processed/procurement_delay_target.csv"

print("=" * 60)
print("STAGE 4.1 — AI DELAY PREDICTION")
print("=" * 60)

# ------------------------------------------------------------
# 1. Load Stage 3 data
# ------------------------------------------------------------

print("\nLoading Stage 3 process analysis data...")

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"Input file not found: {INPUT_FILE}\n"
        "Check the Stage 3 output filename."
    )

df = pd.read_csv(INPUT_FILE)

print(f"Cases loaded: {len(df)}")

# ------------------------------------------------------------
# 2. Check required column
# ------------------------------------------------------------

TIME_COLUMN = "total_processing_time_hours"

if TIME_COLUMN not in df.columns:
    raise ValueError(
        f"Required column '{TIME_COLUMN}' not found.\n"
        f"Available columns:\n{list(df.columns)}"
    )

# ------------------------------------------------------------
# 3. Remove invalid processing times
# ------------------------------------------------------------

df = df[df[TIME_COLUMN].notna()].copy()
df = df[df[TIME_COLUMN] >= 0].copy()

print(f"Valid cases: {len(df)}")

# ------------------------------------------------------------
# 4. Calculate delay threshold
# ------------------------------------------------------------

# Use the 75th percentile:
# cases above this historical processing-time threshold
# are treated as delayed.

delay_threshold = df[TIME_COLUMN].quantile(0.75)

print("\n" + "-" * 60)
print("DELAY THRESHOLD")
print("-" * 60)

print(f"75th percentile processing time: "
      f"{delay_threshold:.2f} hours")

# ------------------------------------------------------------
# 5. Create target
# ------------------------------------------------------------

df["delay_target"] = (
    df[TIME_COLUMN] > delay_threshold
).astype(int)

df["delay_label"] = df["delay_target"].map({
    0: "Not Delayed",
    1: "Delayed"
})

# ------------------------------------------------------------
# 6. Display distribution
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("DELAY CLASS DISTRIBUTION")
print("-" * 60)

distribution = df["delay_label"].value_counts()

print(distribution)

print("\nPercentage distribution:")

percentage = (
    df["delay_label"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(percentage)

# ------------------------------------------------------------
# 7. Save dataset
# ------------------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 60)
print("STAGE 4.1 COMPLETED")
print("=" * 60)

print(f"Output file: {OUTPUT_FILE}")
print(f"Total cases: {len(df)}")
print(f"Delay threshold: {delay_threshold:.2f} hours")

print("\nTarget created:")
print("0 = Not Delayed")
print("1 = Delayed")

print("\nNext step:")
print("Stage 4.2 — Feature Selection & Train/Test Split")