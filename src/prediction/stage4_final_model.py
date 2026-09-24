import pandas as pd
import os
import joblib

from sklearn.linear_model import LogisticRegression

# ============================================================
# STAGE 4.6 — FINAL DELAY PREDICTION PIPELINE
# ============================================================

TRAIN_FILE = "data/processed/train_delay_prediction.csv"
TEST_FILE = "data/processed/test_delay_prediction.csv"

MODEL_FILE = "models/final_delay_prediction_model.pkl"
OUTPUT_FILE = "data/processed/final_delay_predictions.csv"

print("=" * 60)
print("STAGE 4.6 — FINAL DELAY PREDICTION PIPELINE")
print("=" * 60)

# ------------------------------------------------------------
# 1. Load data
# ------------------------------------------------------------

print("\nLoading datasets...")

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

TARGET = "delay_target"

X_train = train_df.drop(columns=[TARGET])
y_train = train_df[TARGET]

X_test = test_df.drop(columns=[TARGET])

print(f"Training cases: {len(X_train)}")
print(f"Prediction cases: {len(X_test)}")
print(f"Features: {X_train.shape[1]}")

# ------------------------------------------------------------
# 2. Train final Logistic Regression model
# ------------------------------------------------------------

print("\nTraining final Logistic Regression model...")

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

print("Final model trained successfully.")

# ------------------------------------------------------------
# 3. Generate probability predictions
# ------------------------------------------------------------

delay_probability = model.predict_proba(X_test)[:, 1]

# ------------------------------------------------------------
# 4. Generate binary predictions
# ------------------------------------------------------------

delay_prediction = (
    delay_probability >= 0.50
).astype(int)

# ------------------------------------------------------------
# 5. Create risk levels
# ------------------------------------------------------------

def assign_risk(probability):

    if probability >= 0.80:
        return "HIGH"

    elif probability >= 0.50:
        return "MEDIUM"

    else:
        return "LOW"


risk_level = [
    assign_risk(probability)
    for probability in delay_probability
]

# ------------------------------------------------------------
# 6. Create final prediction dataset
# ------------------------------------------------------------

results = test_df.copy()

results["delay_probability"] = delay_probability

results["predicted_delay"] = delay_prediction

results["risk_level"] = risk_level

results["prediction_label"] = results[
    "predicted_delay"
].map({
    0: "Not Delayed",
    1: "Delayed"
})

# ------------------------------------------------------------
# 7. Save predictions
# ------------------------------------------------------------

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

results.to_csv(
    OUTPUT_FILE,
    index=False
)

# ------------------------------------------------------------
# 8. Save model
# ------------------------------------------------------------

os.makedirs(
    os.path.dirname(MODEL_FILE),
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)

# ------------------------------------------------------------
# 9. Display prediction summary
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL PREDICTION SUMMARY")
print("=" * 60)

print("\nPredicted classes:")

print(
    results["prediction_label"]
    .value_counts()
)

print("\nRisk levels:")

print(
    results["risk_level"]
    .value_counts()
)

# ------------------------------------------------------------
# 10. Display highest-risk cases
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("TOP 10 HIGHEST-RISK CASES")
print("-" * 60)

top_risk = results.sort_values(
    "delay_probability",
    ascending=False
).head(10)

columns_to_display = [
    "delay_probability",
    "prediction_label",
    "risk_level"
]

print(
    top_risk[
        columns_to_display
    ].to_string(index=False)
)

# ------------------------------------------------------------
# 11. Final output
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STAGE 4.6 COMPLETED")
print("=" * 60)

print(f"Prediction file: {OUTPUT_FILE}")
print(f"Model file     : {MODEL_FILE}")

print("\nAI delay prediction pipeline is ready.")