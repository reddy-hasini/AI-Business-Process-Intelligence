import pandas as pd
from pathlib import Path

# ==========================================
# STAGE 3.3 — PROCESS DEVIATION DETECTION
# ==========================================

INPUT_FILE = Path(
    "data/processed/procurement_process_analysis.csv"
)

print("Loading procurement process data...")

df = pd.read_csv(INPUT_FILE)

print(f"Cases loaded: {len(df)}")

# ==========================================
# CREATE DEVIATION FLAGS
# ==========================================

df["multiple_pr_flag"] = (
    df["pr_count"] > 1
).astype(int)

df["multiple_supplier_flag"] = (
    df["supplier_count"] > 1
).astype(int)

df["multiple_goods_receipt_flag"] = (
    df["goods_receipt_count"] > 1
).astype(int)

df["multiple_invoice_flag"] = (
    df["invoice_count"] > 1
).astype(int)

df["multiple_payment_flag"] = (
    df["payment_count"] > 1
).astype(int)

df["rejection_flag"] = (
    df["rejection_count"] > 0
).astype(int)

# ==========================================
# MATCH RESULT ANALYSIS
# ==========================================

df["match_issue_flag"] = (
    df["match_result"]
    .astype(str)
    .str.lower()
    .isin([
        "mismatch",
        "failed",
        "failure",
        "rejected",
        "exception",
        "unmatched"
    ])
).astype(int)

# ==========================================
# DEVIATION SCORE
# ==========================================

deviation_flags = [
    "multiple_pr_flag",
    "multiple_supplier_flag",
    "multiple_goods_receipt_flag",
    "multiple_invoice_flag",
    "multiple_payment_flag",
    "rejection_flag",
    "match_issue_flag"
]

df["deviation_score"] = df[deviation_flags].sum(axis=1)

# ==========================================
# REWORK SCORE
# ==========================================

df["rework_score"] = (
    (df["pr_count"] - 1).clip(lower=0)
    + (df["goods_receipt_count"] - 1).clip(lower=0)
    + (df["invoice_count"] - 1).clip(lower=0)
    + (df["payment_count"] - 1).clip(lower=0)
    + df["rejection_count"]
)

# ==========================================
# DEVIATION CATEGORY
# ==========================================

def classify_deviation(score):

    if score == 0:
        return "Normal"

    elif score == 1:
        return "Minor Deviation"

    elif score == 2:
        return "Moderate Deviation"

    else:
        return "High Deviation"


df["deviation_category"] = (
    df["deviation_score"]
    .apply(classify_deviation)
)

# ==========================================
# SUMMARY
# ==========================================

print("\n========================================")
print("DEVIATION SUMMARY")
print("========================================")

print(
    df["deviation_category"]
    .value_counts()
    .to_string()
)

# ==========================================
# REWORK SUMMARY
# ==========================================

print("\n========================================")
print("REWORK SUMMARY")
print("========================================")

print(
    f"Cases with rework: "
    f"{(df['rework_score'] > 0).sum()}"
)

print(
    f"Cases without rework: "
    f"{(df['rework_score'] == 0).sum()}"
)

print(
    f"Maximum rework score: "
    f"{df['rework_score'].max()}"
)

# ==========================================
# INDIVIDUAL DEVIATION TYPES
# ==========================================

print("\n========================================")
print("DEVIATION TYPES")
print("========================================")

for column in deviation_flags:

    count = df[column].sum()

    percentage = (
        count / len(df) * 100
    )

    print(
        f"{column:<32} "
        f"{count:>5} cases "
        f"({percentage:.2f}%)"
    )

# ==========================================
# TOP DEVIANT CASES
# ==========================================

print("\n========================================")
print("TOP DEVIANT CASES")
print("========================================")

top_cases = (
    df.sort_values(
        by=["deviation_score", "rework_score"],
        ascending=False
    )
    .head(10)
)

columns_to_show = [
    "case_id",
    "pr_count",
    "supplier_count",
    "goods_receipt_count",
    "invoice_count",
    "payment_count",
    "rejection_count",
    "match_result",
    "deviation_score",
    "rework_score",
    "deviation_category"
]

print(
    top_cases[columns_to_show]
    .to_string(index=False)
)

# ==========================================
# SAVE RESULTS
# ==========================================

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    OUTPUT_DIR /
    "procurement_deviation_analysis.csv"
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n========================================")
print("STAGE 3.3 COMPLETED")
print("========================================")

print(
    f"Output file: {OUTPUT_FILE}"
)