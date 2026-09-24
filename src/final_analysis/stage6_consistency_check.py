import pandas as pd
from pathlib import Path

print("=" * 60)
print("STAGE 6.2 — FINAL DATA CONSISTENCY CHECK")
print("=" * 60)

# ============================================================
# 1. PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STAGE5_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "validated_procurement_recommendations.csv"
)

STAGE6_FILE = (
    BASE_DIR
    / "data"
    / "final"
    / "final_procurement_analysis.csv"
)


# ============================================================
# 2. LOAD DATASETS
# ============================================================

print("\nLoading Stage 5 validated dataset...")

if not STAGE5_FILE.exists():
    raise FileNotFoundError(
        f"Stage 5 file not found:\n{STAGE5_FILE}"
    )

stage5 = pd.read_csv(STAGE5_FILE)

print(f"Stage 5 cases: {len(stage5)}")
print(f"Stage 5 columns: {len(stage5.columns)}")


print("\nLoading Stage 6 final dataset...")

if not STAGE6_FILE.exists():
    raise FileNotFoundError(
        f"Stage 6 file not found:\n{STAGE6_FILE}"
    )

stage6 = pd.read_csv(STAGE6_FILE)

print(f"Stage 6 cases: {len(stage6)}")
print(f"Stage 6 columns: {len(stage6.columns)}")


# ============================================================
# 3. CASE COUNT CHECK
# ============================================================

print("\n" + "=" * 60)
print("1. CASE COUNT CONSISTENCY")
print("=" * 60)

if len(stage5) == len(stage6):
    print("PASS — Both datasets contain the same number of cases.")
else:
    print("WARNING — Case counts are different.")

print(f"Stage 5: {len(stage5)}")
print(f"Stage 6: {len(stage6)}")


# ============================================================
# 4. DELAY COUNT COMPARISON
# ============================================================

print("\n" + "=" * 60)
print("2. DELAY PREDICTION CONSISTENCY")
print("=" * 60)

if "predicted_delay" not in stage5.columns:
    raise KeyError(
        "predicted_delay column missing from Stage 5 dataset."
    )

if "predicted_delay" not in stage6.columns:
    raise KeyError(
        "predicted_delay column missing from Stage 6 dataset."
    )

stage5_delay_counts = stage5["predicted_delay"].value_counts().sort_index()
stage6_delay_counts = stage6["predicted_delay"].value_counts().sort_index()

stage5_delayed = int(
    (stage5["predicted_delay"] == 1).sum()
)

stage5_not_delayed = int(
    (stage5["predicted_delay"] == 0).sum()
)

stage6_delayed = int(
    (stage6["predicted_delay"] == 1).sum()
)

stage6_not_delayed = int(
    (stage6["predicted_delay"] == 0).sum()
)

print("\nStage 5:")
print(f"Delayed:     {stage5_delayed}")
print(f"Not Delayed: {stage5_not_delayed}")

print("\nStage 6:")
print(f"Delayed:     {stage6_delayed}")
print(f"Not Delayed: {stage6_not_delayed}")

if (
    stage5_delayed == stage6_delayed
    and stage5_not_delayed == stage6_not_delayed
):
    print("\nPASS — Delay predictions are consistent.")
else:
    print("\nWARNING — Delay prediction counts differ.")


# ============================================================
# 5. RISK LEVEL COMPARISON
# ============================================================

print("\n" + "=" * 60)
print("3. RISK LEVEL CONSISTENCY")
print("=" * 60)

if "risk_level" in stage5.columns and "risk_level" in stage6.columns:

    stage5_risk = (
        stage5["risk_level"]
        .value_counts()
        .sort_index()
    )

    stage6_risk = (
        stage6["risk_level"]
        .value_counts()
        .sort_index()
    )

    print("\nStage 5 risk distribution:")
    print(stage5_risk)

    print("\nStage 6 risk distribution:")
    print(stage6_risk)

    if stage5_risk.equals(stage6_risk):
        print("\nPASS — Risk distributions are consistent.")
    else:
        print("\nWARNING — Risk distributions differ.")


# ============================================================
# 6. BOTTLENECK COMPARISON
# ============================================================

print("\n" + "=" * 60)
print("4. BOTTLENECK CONSISTENCY")
print("=" * 60)

if (
    "main_bottleneck" in stage5.columns
    and "main_bottleneck" in stage6.columns
):

    stage5_bottlenecks = (
        stage5["main_bottleneck"]
        .value_counts()
        .sort_index()
    )

    stage6_bottlenecks = (
        stage6["main_bottleneck"]
        .value_counts()
        .sort_index()
    )

    print("\nStage 5 bottlenecks:")
    print(stage5_bottlenecks)

    print("\nStage 6 bottlenecks:")
    print(stage6_bottlenecks)

    if stage5_bottlenecks.equals(stage6_bottlenecks):
        print("\nPASS — Bottleneck distributions are consistent.")
    else:
        print("\nWARNING — Bottleneck distributions differ.")


# ============================================================
# 7. ROW-LEVEL CONSISTENCY
# ============================================================

print("\n" + "=" * 60)
print("5. ROW-LEVEL DATA CONSISTENCY")
print("=" * 60)

if len(stage5) == len(stage6):

    common_columns = [
        column
        for column in stage5.columns
        if column in stage6.columns
    ]

    differences = []

    for column in common_columns:

        stage5_values = stage5[column].astype(str).reset_index(drop=True)
        stage6_values = stage6[column].astype(str).reset_index(drop=True)

        mismatch_count = (
            stage5_values != stage6_values
        ).sum()

        if mismatch_count > 0:
            differences.append(
                (column, int(mismatch_count))
            )

    if len(differences) == 0:

        print(
            "PASS — All common columns contain identical "
            "row-level values."
        )

    else:

        print("WARNING — Differences detected:")

        for column, count in differences:
            print(
                f"{column}: {count} mismatched rows"
            )

else:

    print(
        "SKIPPED — Row-level comparison requires "
        "equal case counts."
    )


# ============================================================
# 8. FINAL CONSISTENCY RESULT
# ============================================================

print("\n" + "=" * 60)
print("6. FINAL CONSISTENCY RESULT")
print("=" * 60)

case_count_ok = len(stage5) == len(stage6)

delay_ok = (
    stage5_delayed == stage6_delayed
    and
    stage5_not_delayed == stage6_not_delayed
)

if "risk_level" in stage5.columns and "risk_level" in stage6.columns:
    risk_ok = stage5_risk.equals(stage6_risk)
else:
    risk_ok = True

if (
    "main_bottleneck" in stage5.columns
    and "main_bottleneck" in stage6.columns
):
    bottleneck_ok = stage5_bottlenecks.equals(
        stage6_bottlenecks
    )
else:
    bottleneck_ok = True

print(
    f"Case count consistency: "
    f"{'PASS' if case_count_ok else 'FAIL'}"
)

print(
    f"Delay consistency: "
    f"{'PASS' if delay_ok else 'FAIL'}"
)

print(
    f"Risk consistency: "
    f"{'PASS' if risk_ok else 'FAIL'}"
)

print(
    f"Bottleneck consistency: "
    f"{'PASS' if bottleneck_ok else 'FAIL'}"
)


# ============================================================
# 9. COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("STAGE 6.2 COMPLETED")
print("=" * 60)