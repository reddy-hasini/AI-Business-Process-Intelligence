import pandas as pd
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ============================================================
# STAGE 4.4 — RANDOM FOREST MODEL
# ============================================================

TRAIN_FILE = "data/processed/train_delay_prediction.csv"
TEST_FILE = "data/processed/test_delay_prediction.csv"

print("=" * 60)
print("STAGE 4.4 — RANDOM FOREST MODEL")
print("=" * 60)

# ------------------------------------------------------------
# 1. Load datasets
# ------------------------------------------------------------

print("\nLoading training and testing datasets...")

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

print(f"Training cases: {len(train_df)}")
print(f"Testing cases : {len(test_df)}")

# ------------------------------------------------------------
# 2. Separate features and target
# ------------------------------------------------------------

TARGET = "delay_target"

X_train = train_df.drop(columns=[TARGET])
y_train = train_df[TARGET]

X_test = test_df.drop(columns=[TARGET])
y_test = test_df[TARGET]

print(f"Features used: {X_train.shape[1]}")

# ------------------------------------------------------------
# 3. Train Random Forest
# ------------------------------------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Model training completed.")

# ------------------------------------------------------------
# 4. Generate predictions
# ------------------------------------------------------------

y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)[:, 1]

# ------------------------------------------------------------
# 5. Evaluate model
# ------------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

# ------------------------------------------------------------
# 6. Display performance
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("RANDOM FOREST PERFORMANCE")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

# ------------------------------------------------------------
# 7. Confusion matrix
# ------------------------------------------------------------

cm = confusion_matrix(y_test, y_pred)

print("\n" + "-" * 60)
print("CONFUSION MATRIX")
print("-" * 60)

print("                 Predicted")
print("                 0       1")
print(f"Actual 0      {cm[0,0]:5d}   {cm[0,1]:5d}")
print(f"Actual 1      {cm[1,0]:5d}   {cm[1,1]:5d}")

# ------------------------------------------------------------
# 8. Classification report
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("CLASSIFICATION REPORT")
print("-" * 60)

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Not Delayed", "Delayed"],
        zero_division=0
    )
)

# ------------------------------------------------------------
# 9. Feature importance
# ------------------------------------------------------------

feature_importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    "importance",
    ascending=False
)

print("\n" + "-" * 60)
print("RANDOM FOREST FEATURE IMPORTANCE")
print("-" * 60)

print(
    feature_importance.to_string(index=False)
)

# ------------------------------------------------------------
# 10. Save predictions
# ------------------------------------------------------------

results = test_df.copy()

results["predicted_delay"] = y_pred
results["delay_probability"] = y_probability

OUTPUT_FILE = (
    "data/processed/"
    "random_forest_delay_predictions.csv"
)

results.to_csv(
    OUTPUT_FILE,
    index=False
)

# ------------------------------------------------------------
# 11. Save feature importance
# ------------------------------------------------------------

IMPORTANCE_FILE = (
    "data/processed/"
    "random_forest_feature_importance.csv"
)

feature_importance.to_csv(
    IMPORTANCE_FILE,
    index=False
)

# ------------------------------------------------------------
# 12. Final output
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STAGE 4.4 COMPLETED")
print("=" * 60)

print(f"Prediction output : {OUTPUT_FILE}")
print(f"Feature importance: {IMPORTANCE_FILE}")

print("\nNext step:")
print("Stage 4.5 — Model Comparison & Validation")