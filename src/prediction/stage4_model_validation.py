import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import StratifiedKFold, cross_validate

# ============================================================
# STAGE 4.5 — MODEL COMPARISON & CROSS-VALIDATION
# ============================================================

TRAIN_FILE = "data/processed/train_delay_prediction.csv"
TEST_FILE = "data/processed/test_delay_prediction.csv"

OUTPUT_FILE = "data/processed/model_validation_results.csv"

print("=" * 60)
print("STAGE 4.5 — MODEL COMPARISON & VALIDATION")
print("=" * 60)

# ------------------------------------------------------------
# 1. Load datasets
# ------------------------------------------------------------

print("\nLoading datasets...")

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

TARGET = "delay_target"

X_train = train_df.drop(columns=[TARGET])
y_train = train_df[TARGET]

X_test = test_df.drop(columns=[TARGET])
y_test = test_df[TARGET]

print(f"Training cases: {len(X_train)}")
print(f"Testing cases : {len(X_test)}")
print(f"Features      : {X_train.shape[1]}")

# ------------------------------------------------------------
# 2. Define models
# ------------------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}

# ------------------------------------------------------------
# 3. Define cross-validation
# ------------------------------------------------------------

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scoring = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1",
    "roc_auc": "roc_auc"
}

# ------------------------------------------------------------
# 4. Run cross-validation
# ------------------------------------------------------------

all_results = []

print("\n" + "-" * 60)
print("5-FOLD CROSS-VALIDATION")
print("-" * 60)

for name, model in models.items():

    print(f"\nEvaluating: {name}")

    scores = cross_validate(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,
        n_jobs=-1
    )

    result = {
        "model": name,

        "accuracy_mean":
            scores["test_accuracy"].mean(),

        "accuracy_std":
            scores["test_accuracy"].std(),

        "precision_mean":
            scores["test_precision"].mean(),

        "precision_std":
            scores["test_precision"].std(),

        "recall_mean":
            scores["test_recall"].mean(),

        "recall_std":
            scores["test_recall"].std(),

        "f1_mean":
            scores["test_f1"].mean(),

        "f1_std":
            scores["test_f1"].std(),

        "roc_auc_mean":
            scores["test_roc_auc"].mean(),

        "roc_auc_std":
            scores["test_roc_auc"].std()
    }

    all_results.append(result)

    print(
        f"Accuracy : "
        f"{result['accuracy_mean']:.4f} "
        f"+/- {result['accuracy_std']:.4f}"
    )

    print(
        f"Precision: "
        f"{result['precision_mean']:.4f} "
        f"+/- {result['precision_std']:.4f}"
    )

    print(
        f"Recall   : "
        f"{result['recall_mean']:.4f} "
        f"+/- {result['recall_std']:.4f}"
    )

    print(
        f"F1 Score : "
        f"{result['f1_mean']:.4f} "
        f"+/- {result['f1_std']:.4f}"
    )

    print(
        f"ROC-AUC  : "
        f"{result['roc_auc_mean']:.4f} "
        f"+/- {result['roc_auc_std']:.4f}"
    )

# ------------------------------------------------------------
# 5. Create comparison table
# ------------------------------------------------------------

results_df = pd.DataFrame(all_results)

print("\n" + "=" * 60)
print("MODEL VALIDATION SUMMARY")
print("=" * 60)

display_columns = [
    "model",
    "accuracy_mean",
    "precision_mean",
    "recall_mean",
    "f1_mean",
    "roc_auc_mean"
]

print(
    results_df[display_columns].to_string(index=False)
)

# ------------------------------------------------------------
# 6. Save results
# ------------------------------------------------------------

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("STAGE 4.5 COMPLETED")
print("=" * 60)

print(f"Validation output: {OUTPUT_FILE}")

print("\nNext step:")
print("Stage 4.6 — Final Model Selection & Prediction Pipeline")