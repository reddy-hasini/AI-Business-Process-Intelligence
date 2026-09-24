import pandas as pd
import os
from sklearn.model_selection import train_test_split

# ============================================================
# STAGE 4.2 — FEATURE SELECTION & TRAIN/TEST SPLIT
# ============================================================

INPUT_FILE = "data/processed/procurement_delay_target.csv"

TRAIN_FILE = "data/processed/train_delay_prediction.csv"
TEST_FILE = "data/processed/test_delay_prediction.csv"

print("=" * 60)
print("STAGE 4.2 — FEATURE SELECTION & TRAIN/TEST SPLIT")
print("=" * 60)

# ------------------------------------------------------------
# 1. Load Stage 4.1 dataset
# ------------------------------------------------------------

print("\nLoading delay prediction dataset...")

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"Input file not found: {INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

print(f"Cases loaded: {len(df)}")

# ------------------------------------------------------------
# 2. Define target
# ------------------------------------------------------------

TARGET = "delay_target"

if TARGET not in df.columns:
    raise ValueError(
        f"Target column '{TARGET}' not found."
    )

# ------------------------------------------------------------
# 3. Remove data leakage columns
# ------------------------------------------------------------

# These columns directly reveal the outcome or are labels
# derived from the processing time.

LEAKAGE_COLUMNS = [
    "delay_target",
    "delay_label",
    "total_processing_time_hours"
]

# ------------------------------------------------------------
# 4. Select numeric features
# ------------------------------------------------------------

feature_df = df.drop(
    columns=LEAKAGE_COLUMNS,
    errors="ignore"
)

# Keep numeric columns only
X = feature_df.select_dtypes(
    include=["int64", "float64", "int32", "float32"]
).copy()

y = df[TARGET].copy()

# Remove columns with no predictive information
constant_columns = [
    col for col in X.columns
    if X[col].nunique(dropna=False) <= 1
]

if constant_columns:
    print("\nRemoving constant columns:")
    for col in constant_columns:
        print(f"  - {col}")

    X = X.drop(columns=constant_columns)

# ------------------------------------------------------------
# 5. Handle missing values
# ------------------------------------------------------------

missing_columns = X.columns[X.isnull().any()].tolist()

if missing_columns:
    print("\nMissing values found:")
    for col in missing_columns:
        print(
            f"  - {col}: {X[col].isnull().sum()}"
        )

    # Median imputation
    X = X.fillna(X.median(numeric_only=True))

# ------------------------------------------------------------
# 6. Display selected features
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("SELECTED FEATURES")
print("-" * 60)

for i, column in enumerate(X.columns, start=1):
    print(f"{i:2}. {column}")

print(f"\nTotal features: {X.shape[1]}")

# ------------------------------------------------------------
# 7. Train/test split
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ------------------------------------------------------------
# 8. Combine X and y for saving
# ------------------------------------------------------------

train_df = X_train.copy()
train_df[TARGET] = y_train.values

test_df = X_test.copy()
test_df[TARGET] = y_test.values

# ------------------------------------------------------------
# 9. Save datasets
# ------------------------------------------------------------

os.makedirs(
    os.path.dirname(TRAIN_FILE),
    exist_ok=True
)

train_df.to_csv(TRAIN_FILE, index=False)
test_df.to_csv(TEST_FILE, index=False)

# ------------------------------------------------------------
# 10. Display split information
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("TRAIN / TEST SPLIT")
print("=" * 60)

print(f"Training cases: {len(train_df)}")
print(f"Testing cases : {len(test_df)}")

print("\nTraining target distribution:")
print(
    train_df[TARGET]
    .value_counts()
    .sort_index()
)

print("\nTesting target distribution:")
print(
    test_df[TARGET]
    .value_counts()
    .sort_index()
)

print("\n" + "=" * 60)
print("STAGE 4.2 COMPLETED")
print("=" * 60)

print(f"Training output: {TRAIN_FILE}")
print(f"Testing output : {TEST_FILE}")

print("\nNext step:")
print("Stage 4.3 — Train Baseline ML Model")