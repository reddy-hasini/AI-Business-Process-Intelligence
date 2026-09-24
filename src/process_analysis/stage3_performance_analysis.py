import pandas as pd
from pathlib import Path

# ==========================================
# STAGE 3.4 — PROCESS PERFORMANCE ANALYSIS
# ==========================================

INPUT_FILE = Path(
    "data/processed/procurement_deviation_analysis.csv"
)

print("Loading deviation analysis data...")

df = pd.read_csv(INPUT_FILE)

print(f"Cases loaded: {len(df)}")

# ==========================================
# FIX / REFINE MATCH ISSUE DETECTION
# ==========================================

df["match_issue_flag"] = (
    df["match_result"]
    .astype(str)
    .str.lower()
    .str.contains(
        "mismatch|unmatched|failed|failure|rejected|exception",
        regex=True,
        na=False
    )
).astype(int)

# ==========================================
# PROCESS RISK INDICATORS
# ==========================================

df["long_payment_delay_flag"] = (
    df["match_to_payment_hours"] >
    df["match_to_payment_hours"].median()
).astype(int)

df["long_supplier_delay_flag"] = (
    df["supplier_to_goods_hours"] >
    df["supplier_to_goods_hours"].median()
).astype(int)

df["long_invoice_delay_flag"] = (
    df["goods_to_invoice_hours"] >
    df["goods_to_invoice_hours"].median()
).astype(int)

# ==========================================
# OVERALL PROCESS RISK SCORE
# ==========================================

risk_columns = [
    "rejection_flag",
    "match_issue_flag",
    "multiple_payment_flag",
    "multiple_pr_flag",
    "long_payment_delay_flag",
    "long_supplier_delay_flag",
    "long_invoice_delay_flag"
]

df["process_risk_score"] = df[risk_columns].sum(axis=1)

# ==========================================
# RISK CATEGORY
# ==========================================

def classify_risk(score):

    if score <= 1:
        return "Low Risk"

    elif score <= 3:
        return "Medium Risk"

    else:
        return "High Risk"


df["process_risk_category"] = (
    df["process_risk_score"]
    .apply(classify_risk)
)

# ==========================================
# PROCESS PERFORMANCE SUMMARY
# ==========================================

print("\n========================================")
print("PROCESS PERFORMANCE SUMMARY")
print("========================================")

print(
    df[
        [
            "total_processing_time_hours",
            "deviation_score",
            "rework_score",
            "process_risk_score"
        ]
    ].describe().round(2).to_string()
)

# ==========================================
# RISK DISTRIBUTION
# ==========================================

print("\n========================================")
print("PROCESS RISK DISTRIBUTION")
print("========================================")

risk_summary = (
    df["process_risk_category"]
    .value_counts()
)

for category, count in risk_summary.items():

    percentage = count / len(df) * 100

    print(
        f"{category:<15}"
        f"{count:>5} cases "
        f"({percentage:.2f}%)"
    )

# ==========================================
# HIGH-RISK CASES
# ==========================================

print("\n========================================")
print("TOP HIGH-RISK CASES")
print("========================================")

top_risk_cases = (
    df.sort_values(
        by=[
            "process_risk_score",
            "total_processing_time_hours",
            "rework_score"
        ],
        ascending=False
    )
    .head(15)
)

display_columns = [
    "case_id",
    "total_processing_time_hours",
    "pr_count",
    "supplier_count",
    "goods_receipt_count",
    "invoice_count",
    "payment_count",
    "rejection_count",
    "match_result",
    "deviation_score",
    "rework_score",
    "process_risk_score",
    "process_risk_category"
]

print(
    top_risk_cases[
        display_columns
    ].to_string(index=False)
)

# ==========================================
# BOTTLENECK IMPACT
# ==========================================

print("\n========================================")
print("BOTTLENECK IMPACT")
print("========================================")

bottlenecks = [
    "match_to_payment_hours",
    "supplier_to_goods_hours",
    "goods_to_invoice_hours",
    "pr_to_po_hours",
    "po_approval_hours",
    "invoice_to_match_hours",
    "approval_to_supplier_hours"
]

for column in bottlenecks:

    if column not in df.columns:
        continue

    print(
        f"{column:<32}"
        f"mean={df[column].mean():>8.2f} h | "
        f"median={df[column].median():>8.2f} h"
    )

# ==========================================
# SAVE FINAL STAGE 3 DATASET
# ==========================================

OUTPUT_DIR = Path("data/processed")

OUTPUT_FILE = (
    OUTPUT_DIR /
    "procurement_stage3_final.csv"
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n========================================")
print("STAGE 3.4 COMPLETED")
print("========================================")

print(
    f"Final Stage 3 dataset: {OUTPUT_FILE}"
)