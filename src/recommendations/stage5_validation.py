import pandas as pd
import os

print("=" * 60)
print("STAGE 5.2 — RECOMMENDATION VALIDATION")
print("=" * 60)


# =========================================================
# 1. LOAD STAGE 5 OUTPUT
# =========================================================

input_file = "data/processed/procurement_recommendations.csv"

if not os.path.exists(input_file):
    raise FileNotFoundError(
        f"File not found: {input_file}"
    )

df = pd.read_csv(input_file)

print("\nRecommendation dataset loaded.")
print(f"Cases: {len(df)}")
print(f"Columns: {len(df.columns)}")


# =========================================================
# 2. BASIC VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("1. BASIC DATA VALIDATION")
print("=" * 60)

print("\nMissing values:")

missing = df.isnull().sum()

print(missing[missing > 0])

if missing.sum() == 0:
    print("No missing values found.")


# =========================================================
# 3. RISK / PRIORITY CONSISTENCY
# =========================================================

print("\n" + "=" * 60)
print("2. RISK / PRIORITY CONSISTENCY")
print("=" * 60)

expected_priority = {
    "High": "Immediate",
    "Medium": "Monitor",
    "Low": "Routine"
}

df["priority_expected"] = df["risk_level"].map(
    expected_priority
)

priority_errors = df[
    df["priority"] != df["priority_expected"]
]

print(f"\nPriority consistency errors: {len(priority_errors)}")

if len(priority_errors) == 0:
    print("PASS — All priorities match their risk levels.")
else:
    print(priority_errors[
        ["risk_level", "priority", "priority_expected"]
    ])


# =========================================================
# 4. DELAY / RISK CONSISTENCY
# =========================================================

print("\n" + "=" * 60)
print("3. DELAY / RISK CONSISTENCY")
print("=" * 60)

high_risk_cases = df[
    df["risk_level"] == "High"
]

medium_risk_cases = df[
    df["risk_level"] == "Medium"
]

low_risk_cases = df[
    df["risk_level"] == "Low"
]

print(f"\nHigh-risk cases: {len(high_risk_cases)}")
print(f"Medium-risk cases: {len(medium_risk_cases)}")
print(f"Low-risk cases: {len(low_risk_cases)}")

print("\nPredicted delay by risk level:")

risk_delay_table = pd.crosstab(
    df["risk_level"],
    df["predicted_delay"]
)

print(risk_delay_table)


# =========================================================
# 5. HIGH-RISK RECOMMENDATION VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("4. HIGH-RISK RECOMMENDATION VALIDATION")
print("=" * 60)

high_risk_recommendations = df[
    df["risk_level"] == "High"
]

print(
    f"\nHigh-risk recommendations generated: "
    f"{len(high_risk_recommendations)}"
)

print("\nRecommendation distribution:")

print(
    high_risk_recommendations[
        "recommended_action"
    ].value_counts()
)


# =========================================================
# 6. BOTTLENECK VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("5. BOTTLENECK VALIDATION")
print("=" * 60)

bottleneck_counts = (
    df["main_bottleneck"]
    .value_counts()
)

print("\nBottleneck distribution:")
print(bottleneck_counts)


# =========================================================
# 7. RECOMMENDATION COVERAGE
# =========================================================

print("\n" + "=" * 60)
print("6. RECOMMENDATION COVERAGE")
print("=" * 60)

missing_recommendations = df[
    df["recommended_action"].isna()
    | (df["recommended_action"].str.strip() == "")
]

print(
    f"\nCases without recommendations: "
    f"{len(missing_recommendations)}"
)

if len(missing_recommendations) == 0:
    print("PASS — Every case has a recommendation.")


# =========================================================
# 8. IMMEDIATE PRIORITY VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("7. IMMEDIATE PRIORITY VALIDATION")
print("=" * 60)

immediate_cases = df[
    df["priority"] == "Immediate"
]

print(
    f"\nImmediate-priority cases: "
    f"{len(immediate_cases)}"
)

print("\nImmediate cases by predicted delay:")

print(
    immediate_cases[
        "predicted_delay"
    ].value_counts()
)


# =========================================================
# 9. RECOMMENDATION QUALITY CHECK
# =========================================================

print("\n" + "=" * 60)
print("8. RECOMMENDATION QUALITY CHECK")
print("=" * 60)

quality_issues = []

for index, row in df.iterrows():

    recommendation = str(
        row["recommended_action"]
    ).lower()

    bottleneck = str(
        row["main_bottleneck"]
    ).lower()

    risk = row["risk_level"]

    # High-risk cases should have escalation/
    # corrective-action language
    if risk == "High":

        action_words = [
            "prioritize",
            "escalate",
            "follow up",
            "expedite",
            "review"
        ]

        if not any(
            word in recommendation
            for word in action_words
        ):
            quality_issues.append(
                (index, "High-risk case lacks strong action")
            )

    # Every recommendation must mention some action
    if recommendation.strip() == "":
        quality_issues.append(
            (index, "Empty recommendation")
        )


print(
    f"\nPotential recommendation issues: "
    f"{len(quality_issues)}"
)

if len(quality_issues) == 0:
    print(
        "PASS — Recommendation quality checks completed "
        "without detected issues."
    )
else:

    for issue in quality_issues[:10]:
        print(issue)


# =========================================================
# 10. FINAL VALIDATION SCORE
# =========================================================

print("\n" + "=" * 60)
print("9. FINAL VALIDATION SCORE")
print("=" * 60)

checks = []

# Check 1
checks.append(
    missing.sum() == 0
)

# Check 2
checks.append(
    len(priority_errors) == 0
)

# Check 3
checks.append(
    len(missing_recommendations) == 0
)

# Check 4
checks.append(
    len(quality_issues) == 0
)

passed_checks = sum(checks)
total_checks = len(checks)

validation_score = (
    passed_checks / total_checks
) * 100

print(
    f"\nValidation checks passed: "
    f"{passed_checks}/{total_checks}"
)

print(
    f"Validation score: "
    f"{validation_score:.2f}%"
)


# =========================================================
# 11. SAVE VALIDATED DATA
# =========================================================

df.drop(
    columns=["priority_expected"],
    inplace=True
)

validation_output = (
    "data/processed/"
    "validated_procurement_recommendations.csv"
)

df.to_csv(
    validation_output,
    index=False
)

print("\nValidation output:")
print(validation_output)

print("\n" + "=" * 60)
print("STAGE 5.2 COMPLETED")
print("=" * 60)