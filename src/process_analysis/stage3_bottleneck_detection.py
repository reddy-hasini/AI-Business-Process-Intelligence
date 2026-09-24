import pandas as pd
from pathlib import Path

# ==========================================
# STAGE 3.2 — BOTTLENECK DETECTION
# ==========================================

INPUT_FILE = Path(
    "data/processed/procurement_process_analysis.csv"
)

print("Loading procurement process data...")

df = pd.read_csv(INPUT_FILE)

print(f"Cases loaded: {len(df)}")

# ==========================================
# PROCESS TIME FEATURES
# ==========================================

duration_columns = [
    "pr_to_po_hours",
    "po_approval_hours",
    "approval_to_supplier_hours",
    "supplier_to_goods_hours",
    "goods_to_invoice_hours",
    "invoice_to_match_hours",
    "match_to_payment_hours"
]

available_columns = [
    column for column in duration_columns
    if column in df.columns
]

print("\n========================================")
print("BOTTLENECK ANALYSIS")
print("========================================")

# ==========================================
# CALCULATE STATISTICS
# ==========================================

results = []

for column in available_columns:

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    results.append({
        "process_stage": column,
        "count": len(series),
        "mean_hours": series.mean(),
        "median_hours": series.median(),
        "min_hours": series.min(),
        "max_hours": series.max(),
        "std_hours": series.std(),
        "p75_hours": series.quantile(0.75),
        "p90_hours": series.quantile(0.90),
        "p95_hours": series.quantile(0.95)
    })

bottleneck_df = pd.DataFrame(results)

# ==========================================
# RANK BY AVERAGE PROCESSING TIME
# ==========================================

bottleneck_df = bottleneck_df.sort_values(
    by="mean_hours",
    ascending=False
).reset_index(drop=True)

bottleneck_df["rank_by_mean_time"] = (
    bottleneck_df.index + 1
)

# ==========================================
# PRINT RESULTS
# ==========================================

print("\nProcess stages ranked by average duration:\n")

print(
    bottleneck_df[
        [
            "rank_by_mean_time",
            "process_stage",
            "mean_hours",
            "median_hours",
            "p75_hours",
            "p90_hours",
            "p95_hours",
            "max_hours"
        ]
    ].round(2).to_string(index=False)
)

# ==========================================
# CONTRIBUTION TO TOTAL PROCESS TIME
# ==========================================

print("\n========================================")
print("TIME CONTRIBUTION")
print("========================================")

total_stage_time = bottleneck_df["mean_hours"].sum()

bottleneck_df["time_contribution_percent"] = (
    bottleneck_df["mean_hours"]
    / total_stage_time
    * 100
)

print(
    bottleneck_df[
        [
            "process_stage",
            "mean_hours",
            "time_contribution_percent"
        ]
    ].round(2).to_string(index=False)
)

# ==========================================
# IDENTIFY TOP BOTTLENECK CANDIDATE
# ==========================================

top_stage = bottleneck_df.iloc[0]

print("\n========================================")
print("TOP BOTTLENECK CANDIDATE")
print("========================================")

print(f"Process stage : {top_stage['process_stage']}")
print(f"Average time  : {top_stage['mean_hours']:.2f} hours")
print(f"Median time   : {top_stage['median_hours']:.2f} hours")
print(f"90th percentile: {top_stage['p90_hours']:.2f} hours")
print(f"Maximum time  : {top_stage['max_hours']:.2f} hours")

# ==========================================
# SAVE RESULTS
# ==========================================

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = (
    OUTPUT_DIR /
    "procurement_bottleneck_analysis.csv"
)

bottleneck_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n========================================")
print("STAGE 3.2 COMPLETED")
print("========================================")

print(f"Output file: {OUTPUT_FILE}")