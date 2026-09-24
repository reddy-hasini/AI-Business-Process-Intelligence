import pandas as pd
import os

print("=" * 60)
print("STAGE 5 — PROCUREMENT RECOMMENDATION ENGINE")
print("=" * 60)


# =========================================================
# 1. LOAD STAGE 4 PREDICTIONS
# =========================================================

input_file = "data/processed/random_forest_delay_predictions.csv"

if not os.path.exists(input_file):
    raise FileNotFoundError(
        f"Input file not found: {input_file}"
    )

df = pd.read_csv(input_file)

print("\nStage 4 prediction data loaded successfully.")
print(f"Cases: {len(df)}")
print(f"Features: {len(df.columns)}")


# =========================================================
# 2. CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "pr_count",
    "supplier_count",
    "goods_receipt_count",
    "invoice_count",
    "payment_count",
    "pr_to_po_hours",
    "po_approval_hours",
    "approval_to_supplier_hours",
    "supplier_to_goods_hours",
    "goods_to_invoice_hours",
    "invoice_to_match_hours",
    "match_to_payment_hours",
    "rejection_count",
    "predicted_delay",
    "delay_probability"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("\nColumn validation successful.")


# =========================================================
# 3. CREATE RISK LEVEL
# =========================================================

def calculate_risk(probability):

    if probability >= 0.75:
        return "High"

    elif probability >= 0.40:
        return "Medium"

    else:
        return "Low"


df["risk_level"] = df["delay_probability"].apply(
    calculate_risk
)


# =========================================================
# 4. IDENTIFY MAIN BOTTLENECK
# =========================================================

time_columns = {
    "PR to PO": "pr_to_po_hours",
    "PO Approval": "po_approval_hours",
    "Approval to Supplier": "approval_to_supplier_hours",
    "Supplier to Goods Receipt": "supplier_to_goods_hours",
    "Goods Receipt to Invoice": "goods_to_invoice_hours",
    "Invoice to Matching": "invoice_to_match_hours",
    "Matching to Payment": "match_to_payment_hours"
}


def identify_bottleneck(row):

    values = {
        stage: row[column]
        for stage, column in time_columns.items()
    }

    bottleneck = max(values, key=values.get)

    return bottleneck


df["main_bottleneck"] = df.apply(
    identify_bottleneck,
    axis=1
)


# =========================================================
# 5. GENERATE RECOMMENDATION
# =========================================================

def generate_recommendation(row):

    risk = row["risk_level"]
    bottleneck = row["main_bottleneck"]

    rejection_count = row["rejection_count"]

    # ---------------------------------------------
    # HIGH RISK
    # ---------------------------------------------

    if risk == "High":

        if rejection_count > 0:
            return (
                "Prioritize procurement case and review "
                "rejected transactions before further processing."
            )

        elif bottleneck == "PO Approval":
            return (
                "Prioritize purchase order approval "
                "and escalate pending approvals."
            )

        elif bottleneck == "Approval to Supplier":
            return (
                "Follow up with supplier immediately "
                "after internal approval."
            )

        elif bottleneck == "Supplier to Goods Receipt":
            return (
                "Contact supplier and expedite "
                "delivery of ordered goods."
            )

        elif bottleneck == "Goods Receipt to Invoice":
            return (
                "Review invoice submission process "
                "and resolve receipt-to-invoice delays."
            )

        elif bottleneck == "Invoice to Matching":
            return (
                "Review invoice matching issues "
                "and resolve discrepancies."
            )

        elif bottleneck == "Matching to Payment":
            return (
                "Prioritize invoice matching and "
                "payment processing."
            )

        else:
            return (
                "Escalate procurement case for "
                "immediate process review."
            )


    # ---------------------------------------------
    # MEDIUM RISK
    # ---------------------------------------------

    elif risk == "Medium":

        if rejection_count > 0:
            return (
                "Review rejected transactions and "
                "monitor the procurement case closely."
            )

        elif bottleneck == "PO Approval":
            return (
                "Monitor purchase order approval "
                "and follow up if processing continues."
            )

        elif bottleneck == "Supplier to Goods Receipt":
            return (
                "Monitor supplier delivery progress "
                "and follow up if delayed."
            )

        elif bottleneck == "Matching to Payment":
            return (
                "Monitor invoice matching and "
                "payment processing."
            )

        else:
            return (
                "Monitor the identified process bottleneck "
                "and take corrective action if delay increases."
            )


    # ---------------------------------------------
    # LOW RISK
    # ---------------------------------------------

    else:

        return (
            "Continue normal procurement processing "
            "with routine monitoring."
        )


df["recommended_action"] = df.apply(
    generate_recommendation,
    axis=1
)


# =========================================================
# 6. ASSIGN PRIORITY
# =========================================================

def assign_priority(risk):

    if risk == "High":
        return "Immediate"

    elif risk == "Medium":
        return "Monitor"

    else:
        return "Routine"


df["priority"] = df["risk_level"].apply(
    assign_priority
)


# =========================================================
# 7. CREATE FINAL RECOMMENDATION DATASET
# =========================================================

output_columns = [
    "pr_count",
    "supplier_count",
    "goods_receipt_count",
    "invoice_count",
    "payment_count",
    "pr_to_po_hours",
    "po_approval_hours",
    "approval_to_supplier_hours",
    "supplier_to_goods_hours",
    "goods_to_invoice_hours",
    "invoice_to_match_hours",
    "match_to_payment_hours",
    "rejection_count",
    "predicted_delay",
    "delay_probability",
    "risk_level",
    "main_bottleneck",
    "priority",
    "recommended_action"
]

recommendation_df = df[output_columns].copy()


# =========================================================
# 8. SAVE OUTPUT
# =========================================================

output_file = (
    "data/processed/procurement_recommendations.csv"
)

recommendation_df.to_csv(
    output_file,
    index=False
)


# =========================================================
# 9. DISPLAY SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("STAGE 5 RECOMMENDATION SUMMARY")
print("=" * 60)

print("\nRisk distribution:")
print(
    recommendation_df["risk_level"].value_counts()
)

print("\nPriority distribution:")
print(
    recommendation_df["priority"].value_counts()
)

print("\nMain bottlenecks:")
print(
    recommendation_df["main_bottleneck"].value_counts()
)

print("\nPredicted delay distribution:")
print(
    recommendation_df["predicted_delay"].value_counts()
)

print("\nOutput file:")
print(output_file)

print("\nStage 5 completed successfully.")