import pandas as pd
from pathlib import Path

print("=" * 60)
print("STAGE 6.1 — FINAL INTEGRATED PROCUREMENT ANALYSIS")
print("=" * 60)

# ============================================================
# 1. PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "validated_procurement_recommendations.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "final_procurement_analysis.csv"


# ============================================================
# 2. LOAD DATA
# ============================================================

print("\nLoading validated recommendation dataset...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Input file not found:\n{INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

print(f"Cases loaded: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 3. BASIC VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("1. BASIC DATA VALIDATION")
print("=" * 60)

print("\nMissing values:")

missing = df.isnull().sum()
missing = missing[missing > 0]

if len(missing) == 0:
    print("No missing values found.")
else:
    print(missing)


# ============================================================
# 4. DELAY SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("2. DELAY PREDICTION SUMMARY")
print("=" * 60)

if "predicted_delay" in df.columns:

    delay_counts = df["predicted_delay"].value_counts().sort_index()

    delayed = int(delay_counts.get(1, 0))
    not_delayed = int(delay_counts.get(0, 0))

    print(f"\nPredicted Delayed:     {delayed}")
    print(f"Predicted Not Delayed: {not_delayed}")

    print("\nDelay distribution:")
    print(df["predicted_delay"].value_counts())


# ============================================================
# 5. RISK SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("3. RISK LEVEL SUMMARY")
print("=" * 60)

if "risk_level" in df.columns:

    risk_counts = df["risk_level"].value_counts()

    print("\nRisk distribution:")
    print(risk_counts)

    for level in ["High", "Medium", "Low"]:
        print(
            f"{level} Risk: "
            f"{int(risk_counts.get(level, 0))}"
        )


# ============================================================
# 6. BOTTLENECK SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("4. PROCESS BOTTLENECK SUMMARY")
print("=" * 60)

if "main_bottleneck" in df.columns:

    bottleneck_counts = (
        df["main_bottleneck"]
        .value_counts()
    )

    print("\nMain bottlenecks:")
    print(bottleneck_counts)


# ============================================================
# 7. RECOMMENDATION SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("5. RECOMMENDATION SUMMARY")
print("=" * 60)

if "recommended_action" in df.columns:

    recommendation_counts = (
        df["recommended_action"]
        .value_counts()
    )

    print("\nRecommended actions:")
    print(recommendation_counts)

    recommendation_coverage = (
        df["recommended_action"]
        .notna()
        .sum()
    )

    print(
        f"\nRecommendation coverage: "
        f"{recommendation_coverage}/{len(df)}"
    )


# ============================================================
# 8. PRIORITY SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("6. PRIORITY SUMMARY")
print("=" * 60)

if "priority" in df.columns:

    priority_counts = df["priority"].value_counts()

    print("\nPriority distribution:")
    print(priority_counts)


# ============================================================
# 9. HIGH-RISK ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("7. HIGH-RISK CASE ANALYSIS")
print("=" * 60)

if "risk_level" in df.columns:

    high_risk = df[df["risk_level"] == "High"]

    print(f"\nHigh-risk cases: {len(high_risk)}")

    if "predicted_delay" in high_risk.columns:

        high_risk_delayed = (
            high_risk["predicted_delay"] == 1
        ).sum()

        print(
            f"High-risk cases predicted delayed: "
            f"{high_risk_delayed}"
        )


# ============================================================
# 10. IMMEDIATE PRIORITY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("8. IMMEDIATE PRIORITY ANALYSIS")
print("=" * 60)

if "priority" in df.columns:

    immediate = df[
        df["priority"]
        .astype(str)
        .str.lower()
        .str.contains("immediate")
    ]

    print(
        f"\nImmediate-priority cases: "
        f"{len(immediate)}"
    )

    if "predicted_delay" in immediate.columns:

        immediate_delayed = (
            immediate["predicted_delay"] == 1
        ).sum()

        print(
            f"Immediate-priority cases predicted delayed: "
            f"{immediate_delayed}"
        )


# ============================================================
# 11. FINAL KPI SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("9. FINAL PROJECT KPI SUMMARY")
print("=" * 60)

total_cases = len(df)

print(f"\nTotal procurement cases: {total_cases}")

if "predicted_delay" in df.columns:

    delayed = int(
        (df["predicted_delay"] == 1).sum()
    )

    not_delayed = int(
        (df["predicted_delay"] == 0).sum()
    )

    delay_rate = (
        delayed / total_cases * 100
        if total_cases > 0
        else 0
    )

    print(f"Predicted delayed cases: {delayed}")
    print(f"Predicted non-delayed cases: {not_delayed}")
    print(f"Predicted delay rate: {delay_rate:.2f}%")


if "risk_level" in df.columns:

    high = int(
        (df["risk_level"] == "High").sum()
    )

    medium = int(
        (df["risk_level"] == "Medium").sum()
    )

    low = int(
        (df["risk_level"] == "Low").sum()
    )

    print(f"High-risk cases: {high}")
    print(f"Medium-risk cases: {medium}")
    print(f"Low-risk cases: {low}")


if "recommended_action" in df.columns:

    coverage = (
        df["recommended_action"]
        .notna()
        .sum()
    )

    coverage_rate = (
        coverage / total_cases * 100
        if total_cases > 0
        else 0
    )

    print(
        f"Recommendation coverage: "
        f"{coverage_rate:.2f}%"
    )


# ============================================================
# 12. SAVE FINAL DATASET
# ============================================================

print("\n" + "=" * 60)
print("10. SAVING FINAL DATASET")
print("=" * 60)

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nFinal dataset saved to:")
print(OUTPUT_FILE)


# ============================================================
# 13. COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("STAGE 6.1 COMPLETED")
print("=" * 60)