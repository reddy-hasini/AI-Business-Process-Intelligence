import pandas as pd
from pathlib import Path

print("=" * 60)
print("STAGE 6.3 — FINAL KPI & BUSINESS INSIGHTS REPORT")
print("=" * 60)

# ============================================================
# 1. PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "final"
    / "final_procurement_analysis.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = OUTPUT_DIR / "stage6_business_insights.txt"
KPI_FILE = OUTPUT_DIR / "stage6_kpi_summary.csv"


# ============================================================
# 2. LOAD FINAL DATASET
# ============================================================

print("\nLoading final integrated dataset...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Final dataset not found:\n{INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

total_cases = len(df)

print(f"Cases loaded: {total_cases}")
print(f"Columns loaded: {len(df.columns)}")


# ============================================================
# 3. CALCULATE KPIs
# ============================================================

# Delay
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


# Risk
high_risk = int(
    (df["risk_level"] == "High").sum()
)

medium_risk = int(
    (df["risk_level"] == "Medium").sum()
)

low_risk = int(
    (df["risk_level"] == "Low").sum()
)


# Recommendations
recommendation_coverage = int(
    df["recommended_action"].notna().sum()
)

recommendation_rate = (
    recommendation_coverage / total_cases * 100
    if total_cases > 0
    else 0
)


# Immediate priority
immediate_priority = int(
    df["priority"]
    .astype(str)
    .str.lower()
    .str.contains("immediate")
    .sum()
)


# High-risk delayed
high_risk_delayed = int(
    (
        (df["risk_level"] == "High")
        &
        (df["predicted_delay"] == 1)
    ).sum()
)


# ============================================================
# 4. DISTRIBUTIONS
# ============================================================

risk_distribution = (
    df["risk_level"]
    .value_counts()
)

bottleneck_distribution = (
    df["main_bottleneck"]
    .value_counts()
)

recommendation_distribution = (
    df["recommended_action"]
    .value_counts()
)

priority_distribution = (
    df["priority"]
    .value_counts()
)


# ============================================================
# 5. TOP BOTTLENECK
# ============================================================

top_bottleneck = (
    bottleneck_distribution.index[0]
    if len(bottleneck_distribution) > 0
    else "N/A"
)

top_bottleneck_cases = (
    int(bottleneck_distribution.iloc[0])
    if len(bottleneck_distribution) > 0
    else 0
)

top_bottleneck_percentage = (
    top_bottleneck_cases / total_cases * 100
    if total_cases > 0
    else 0
)


# ============================================================
# 6. TOP RECOMMENDATION
# ============================================================

top_recommendation = (
    recommendation_distribution.index[0]
    if len(recommendation_distribution) > 0
    else "N/A"
)

top_recommendation_cases = (
    int(recommendation_distribution.iloc[0])
    if len(recommendation_distribution) > 0
    else 0
)


# ============================================================
# 7. DISPLAY KPI SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("1. FINAL KPI SUMMARY")
print("=" * 60)

print(f"\nTotal procurement cases:       {total_cases}")
print(f"Predicted delayed cases:       {delayed}")
print(f"Predicted non-delayed cases:   {not_delayed}")
print(f"Predicted delay rate:          {delay_rate:.2f}%")

print(f"\nHigh-risk cases:                {high_risk}")
print(f"Medium-risk cases:              {medium_risk}")
print(f"Low-risk cases:                 {low_risk}")

print(f"\nImmediate-priority cases:       {immediate_priority}")
print(f"High-risk + delayed cases:     {high_risk_delayed}")

print(
    f"\nRecommendation coverage:        "
    f"{recommendation_rate:.2f}%"
)


# ============================================================
# 8. RISK ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("2. RISK ANALYSIS")
print("=" * 60)

print("\nRisk distribution:")

for level in ["High", "Medium", "Low"]:
    count = int(risk_distribution.get(level, 0))

    percentage = (
        count / total_cases * 100
        if total_cases > 0
        else 0
    )

    print(
        f"{level:8s}: {count:3d} cases "
        f"({percentage:.2f}%)"
    )


# ============================================================
# 9. BOTTLENECK ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("3. PROCESS BOTTLENECK ANALYSIS")
print("=" * 60)

for bottleneck, count in bottleneck_distribution.items():

    percentage = (
        count / total_cases * 100
        if total_cases > 0
        else 0
    )

    print(
        f"{bottleneck}: "
        f"{count} cases ({percentage:.2f}%)"
    )

print(
    f"\nDominant bottleneck: {top_bottleneck}"
)

print(
    f"Cases affected: {top_bottleneck_cases}"
)

print(
    f"Share of cases: {top_bottleneck_percentage:.2f}%"
)


# ============================================================
# 10. RECOMMENDATION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("4. RECOMMENDATION ANALYSIS")
print("=" * 60)

for recommendation, count in recommendation_distribution.items():

    print(
        f"{recommendation}: {count}"
    )

print(
    f"\nMost frequent recommendation: "
    f"{top_recommendation}"
)

print(
    f"Cases receiving this recommendation: "
    f"{top_recommendation_cases}"
)


# ============================================================
# 11. PRIORITY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("5. PRIORITY ANALYSIS")
print("=" * 60)

for priority, count in priority_distribution.items():

    percentage = (
        count / total_cases * 100
        if total_cases > 0
        else 0
    )

    print(
        f"{priority}: "
        f"{count} cases ({percentage:.2f}%)"
    )


# ============================================================
# 12. BUSINESS INSIGHTS
# ============================================================

print("\n" + "=" * 60)
print("6. KEY BUSINESS INSIGHTS")
print("=" * 60)

insights = []

insights.append(
    f"The system analyzed {total_cases} procurement cases "
    f"and predicted {delayed} cases as delayed, representing "
    f"a predicted delay rate of {delay_rate:.2f}%."
)

insights.append(
    f"There are {high_risk} high-risk procurement cases, "
    f"and all {high_risk_delayed} high-risk cases are predicted "
    f"to experience delays."
)

insights.append(
    f"The dominant process bottleneck is "
    f"'{top_bottleneck}', affecting "
    f"{top_bottleneck_cases} cases "
    f"({top_bottleneck_percentage:.2f}% of the dataset)."
)

insights.append(
    f"The system generated recommendations for all "
    f"{recommendation_coverage} cases, resulting in "
    f"{recommendation_rate:.2f}% recommendation coverage."
)

insights.append(
    f"{immediate_priority} cases were classified as "
    f"immediate priority and require attention based on "
    f"the integrated risk and prediction results."
)

for number, insight in enumerate(insights, start=1):
    print(f"\n{number}. {insight}")


# ============================================================
# 13. KPI DATAFRAME
# ============================================================

kpi_data = {
    "KPI": [
        "Total Cases",
        "Predicted Delayed Cases",
        "Predicted Non-Delayed Cases",
        "Predicted Delay Rate (%)",
        "High-Risk Cases",
        "Medium-Risk Cases",
        "Low-Risk Cases",
        "Immediate-Priority Cases",
        "High-Risk Delayed Cases",
        "Recommendation Coverage (%)",
        "Top Bottleneck",
        "Top Bottleneck Cases",
        "Top Bottleneck Share (%)",
    ],
    "Value": [
        total_cases,
        delayed,
        not_delayed,
        round(delay_rate, 2),
        high_risk,
        medium_risk,
        low_risk,
        immediate_priority,
        high_risk_delayed,
        round(recommendation_rate, 2),
        top_bottleneck,
        top_bottleneck_cases,
        round(top_bottleneck_percentage, 2),
    ],
}

kpi_df = pd.DataFrame(kpi_data)


# ============================================================
# 14. SAVE KPI SUMMARY
# ============================================================

kpi_df.to_csv(
    KPI_FILE,
    index=False
)

print("\n" + "=" * 60)
print("7. KPI SUMMARY SAVED")
print("=" * 60)

print(f"\nSaved to:")
print(KPI_FILE)


# ============================================================
# 15. SAVE BUSINESS INSIGHTS REPORT
# ============================================================

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 6.3 — FINAL KPI & BUSINESS INSIGHTS REPORT\n"
    )

    file.write("=" * 60 + "\n\n")

    file.write("FINAL KPI SUMMARY\n")
    file.write("-" * 60 + "\n")

    file.write(
        f"Total procurement cases: {total_cases}\n"
    )

    file.write(
        f"Predicted delayed cases: {delayed}\n"
    )

    file.write(
        f"Predicted non-delayed cases: {not_delayed}\n"
    )

    file.write(
        f"Predicted delay rate: {delay_rate:.2f}%\n"
    )

    file.write(
        f"High-risk cases: {high_risk}\n"
    )

    file.write(
        f"Medium-risk cases: {medium_risk}\n"
    )

    file.write(
        f"Low-risk cases: {low_risk}\n"
    )

    file.write(
        f"Immediate-priority cases: {immediate_priority}\n"
    )

    file.write(
        f"High-risk + delayed cases: {high_risk_delayed}\n"
    )

    file.write(
        f"Recommendation coverage: "
        f"{recommendation_rate:.2f}%\n\n"
    )

    file.write("PROCESS BOTTLENECKS\n")
    file.write("-" * 60 + "\n")

    for bottleneck, count in bottleneck_distribution.items():

        percentage = (
            count / total_cases * 100
            if total_cases > 0
            else 0
        )

        file.write(
            f"{bottleneck}: "
            f"{count} cases ({percentage:.2f}%)\n"
        )

    file.write("\nKEY BUSINESS INSIGHTS\n")
    file.write("-" * 60 + "\n")

    for number, insight in enumerate(insights, start=1):
        file.write(
            f"{number}. {insight}\n"
        )


# ============================================================
# 16. COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("8. REPORT SAVED")
print("=" * 60)

print(f"\nBusiness insights report:")
print(REPORT_FILE)

print("\n" + "=" * 60)
print("STAGE 6.3 COMPLETED")
print("=" * 60)