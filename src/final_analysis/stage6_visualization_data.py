import pandas as pd
from pathlib import Path

print("=" * 60)
print("STAGE 6.4 — FINAL VISUALIZATION DATA PREPARATION")
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

OUTPUT_DIR = BASE_DIR / "data" / "final" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD FINAL DATASET
# ============================================================

print("\nLoading final integrated dataset...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Final dataset not found:\n{INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

print(f"Cases loaded: {len(df)}")
print(f"Columns loaded: {len(df.columns)}")


# ============================================================
# 3. RISK DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("1. RISK DISTRIBUTION DATA")
print("=" * 60)

risk_data = (
    df["risk_level"]
    .value_counts()
    .rename_axis("risk_level")
    .reset_index(name="case_count")
)

risk_data["percentage"] = (
    risk_data["case_count"]
    / len(df)
    * 100
)

risk_file = OUTPUT_DIR / "risk_distribution.csv"
risk_data.to_csv(risk_file, index=False)

print(risk_data)
print(f"\nSaved: {risk_file}")


# ============================================================
# 4. DELAY DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("2. DELAY DISTRIBUTION DATA")
print("=" * 60)

delay_data = (
    df["predicted_delay"]
    .map({
        0: "Not Delayed",
        1: "Delayed"
    })
    .value_counts()
    .rename_axis("prediction_label")
    .reset_index(name="case_count")
)

delay_data["percentage"] = (
    delay_data["case_count"]
    / len(df)
    * 100
)

delay_file = OUTPUT_DIR / "delay_distribution.csv"
delay_data.to_csv(delay_file, index=False)

print(delay_data)
print(f"\nSaved: {delay_file}")


# ============================================================
# 5. BOTTLENECK DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("3. BOTTLENECK DISTRIBUTION DATA")
print("=" * 60)

bottleneck_data = (
    df["main_bottleneck"]
    .value_counts()
    .rename_axis("main_bottleneck")
    .reset_index(name="case_count")
)

bottleneck_data["percentage"] = (
    bottleneck_data["case_count"]
    / len(df)
    * 100
)

bottleneck_file = (
    OUTPUT_DIR / "bottleneck_distribution.csv"
)

bottleneck_data.to_csv(
    bottleneck_file,
    index=False
)

print(bottleneck_data)
print(f"\nSaved: {bottleneck_file}")


# ============================================================
# 6. PRIORITY DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("4. PRIORITY DISTRIBUTION DATA")
print("=" * 60)

priority_data = (
    df["priority"]
    .value_counts()
    .rename_axis("priority")
    .reset_index(name="case_count")
)

priority_data["percentage"] = (
    priority_data["case_count"]
    / len(df)
    * 100
)

priority_file = (
    OUTPUT_DIR / "priority_distribution.csv"
)

priority_data.to_csv(
    priority_file,
    index=False
)

print(priority_data)
print(f"\nSaved: {priority_file}")


# ============================================================
# 7. RECOMMENDATION DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("5. RECOMMENDATION DISTRIBUTION DATA")
print("=" * 60)

recommendation_data = (
    df["recommended_action"]
    .value_counts()
    .rename_axis("recommended_action")
    .reset_index(name="case_count")
)

recommendation_data["percentage"] = (
    recommendation_data["case_count"]
    / len(df)
    * 100
)

recommendation_file = (
    OUTPUT_DIR / "recommendation_distribution.csv"
)

recommendation_data.to_csv(
    recommendation_file,
    index=False
)

print(recommendation_data)
print(f"\nSaved: {recommendation_file}")


# ============================================================
# 8. RISK VS DELAY MATRIX
# ============================================================

print("\n" + "=" * 60)
print("6. RISK VS DELAY MATRIX")
print("=" * 60)

risk_delay = pd.crosstab(
    df["risk_level"],
    df["predicted_delay"]
)

risk_delay = risk_delay.rename(
    columns={
        0: "Not Delayed",
        1: "Delayed"
    }
)

risk_delay = risk_delay.reset_index()

risk_delay_file = (
    OUTPUT_DIR / "risk_vs_delay.csv"
)

risk_delay.to_csv(
    risk_delay_file,
    index=False
)

print(risk_delay)
print(f"\nSaved: {risk_delay_file}")


# ============================================================
# 9. RISK VS BOTTLENECK
# ============================================================

print("\n" + "=" * 60)
print("7. RISK VS BOTTLENECK")
print("=" * 60)

risk_bottleneck = pd.crosstab(
    df["main_bottleneck"],
    df["risk_level"]
)

risk_bottleneck = risk_bottleneck.reset_index()

risk_bottleneck_file = (
    OUTPUT_DIR / "risk_vs_bottleneck.csv"
)

risk_bottleneck.to_csv(
    risk_bottleneck_file,
    index=False
)

print(risk_bottleneck)
print(f"\nSaved: {risk_bottleneck_file}")


# ============================================================
# 10. PRIORITY VS DELAY
# ============================================================

print("\n" + "=" * 60)
print("8. PRIORITY VS DELAY")
print("=" * 60)

priority_delay = pd.crosstab(
    df["priority"],
    df["predicted_delay"]
)

priority_delay = priority_delay.rename(
    columns={
        0: "Not Delayed",
        1: "Delayed"
    }
)

priority_delay = priority_delay.reset_index()

priority_delay_file = (
    OUTPUT_DIR / "priority_vs_delay.csv"
)

priority_delay.to_csv(
    priority_delay_file,
    index=False
)

print(priority_delay)
print(f"\nSaved: {priority_delay_file}")


# ============================================================
# 11. DASHBOARD KPI FILE
# ============================================================

print("\n" + "=" * 60)
print("9. DASHBOARD KPI DATA")
print("=" * 60)

total_cases = len(df)

delayed = int(
    (df["predicted_delay"] == 1).sum()
)

not_delayed = int(
    (df["predicted_delay"] == 0).sum()
)

high_risk = int(
    (df["risk_level"] == "High").sum()
)

medium_risk = int(
    (df["risk_level"] == "Medium").sum()
)

low_risk = int(
    (df["risk_level"] == "Low").sum()
)

immediate = int(
    df["priority"]
    .astype(str)
    .str.lower()
    .str.contains("immediate")
    .sum()
)

dashboard_kpi = pd.DataFrame({
    "metric": [
        "Total Cases",
        "Predicted Delayed",
        "Predicted Not Delayed",
        "Predicted Delay Rate",
        "High Risk",
        "Medium Risk",
        "Low Risk",
        "Immediate Priority",
        "Recommendation Coverage"
    ],
    "value": [
        total_cases,
        delayed,
        not_delayed,
        round(delayed / total_cases * 100, 2),
        high_risk,
        medium_risk,
        low_risk,
        immediate,
        100.00
    ]
})

dashboard_file = (
    OUTPUT_DIR / "dashboard_kpis.csv"
)

dashboard_kpi.to_csv(
    dashboard_file,
    index=False
)

print(dashboard_kpi)
print(f"\nSaved: {dashboard_file}")


# ============================================================
# 12. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("10. VISUALIZATION DATA SUMMARY")
print("=" * 60)

print(
    f"\nVisualization datasets created successfully."
)

print(
    f"Output directory:\n{OUTPUT_DIR}"
)

print("\nFiles created:")

for file in sorted(OUTPUT_DIR.glob("*.csv")):
    print(f" - {file.name}")


# ============================================================
# 13. COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("STAGE 6.4 COMPLETED")
print("=" * 60)