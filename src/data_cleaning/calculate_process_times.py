import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RELATIONS_FILE = "data/processed/event_object_relations.csv"
EVENTS_FILE = "data/processed/events.csv"
OBJECTS_FILE = "data/processed/objects.csv"
TRANSACTION_FILE = "data/processed/procurement_cases.csv"

OUTPUT_FILE = "data/processed/procurement_timing_features.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading data...")

relations = pd.read_csv(RELATIONS_FILE)
events = pd.read_csv(EVENTS_FILE)
objects = pd.read_csv(OBJECTS_FILE)
transactions = pd.read_csv(TRANSACTION_FILE)

print(f"Relations loaded: {len(relations)}")
print(f"Events loaded: {len(events)}")
print(f"Objects loaded: {len(objects)}")
print(f"Transactions loaded: {len(transactions)}")


# ============================================================
# PREPARE RELATIONSHIPS
# ============================================================

relations = relations.merge(
    objects[["object_id", "object_type"]],
    on="object_id",
    how="left"
)

event_relations = relations.merge(
    events,
    on="event_id",
    how="left"
)

event_relations["timestamp"] = pd.to_datetime(
    event_relations["timestamp"],
    errors="coerce"
)

print("\nTimestamp conversion completed.")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_event_time(rows, event_types):

    filtered = rows[
        rows["event_type"].isin(event_types)
    ]["timestamp"].dropna()

    if filtered.empty:
        return pd.NaT

    return filtered.min()


def hours_between(start, end):

    if pd.isna(start) or pd.isna(end):
        return None

    seconds = (end - start).total_seconds()

    return round(seconds / 3600, 3)


# ============================================================
# CALCULATE PO-LEVEL FEATURES
# ============================================================

results = []

for _, transaction in transactions.iterrows():

    po_id = transaction["po_id"]

    # ========================================================
    # 1. FIND EVENTS DIRECTLY CONNECTED TO PO
    # ========================================================

    po_rows = event_relations[
        event_relations["object_id"] == po_id
    ]

    po_event_ids = (
        po_rows["event_id"]
        .dropna()
        .unique()
    )

    direct_po_events = event_relations[
        event_relations["event_id"].isin(po_event_ids)
    ].copy()

    # ========================================================
    # 2. GET PR IDs
    # ========================================================

    pr_ids = transaction["pr_ids"]

    if pd.isna(pr_ids) or str(pr_ids).strip() == "":
        pr_list = []
    else:
        pr_list = [
            x.strip()
            for x in str(pr_ids).split(";")
            if x.strip()
        ]

    # ========================================================
    # 3. GET PR EVENTS
    # ========================================================

    pr_events = event_relations[
        event_relations["object_id"].isin(pr_list)
    ].copy()

    # ========================================================
    # 4. PR TIMESTAMPS
    # ========================================================

    pr_creation = get_event_time(
        pr_events,
        ["Create PR"]
    )

    pr_approval = get_event_time(
        pr_events,
        ["Approve PR"]
    )

    rejection_count = (
        pr_events[
            pr_events["event_type"] == "Reject PR"
        ]["event_id"]
        .nunique()
    )

    # ========================================================
    # 5. PO TIMESTAMPS
    # ========================================================

    po_creation = get_event_time(
        direct_po_events,
        [
            "Create PO",
            "Create PO (Batch)"
        ]
    )

    po_approval = get_event_time(
        direct_po_events,
        ["Approve PO"]
    )

    po_sent = get_event_time(
        direct_po_events,
        ["Send PO to Supplier"]
    )

    goods_received = get_event_time(
        direct_po_events,
        ["Receive Goods"]
    )

    invoice_received = get_event_time(
        direct_po_events,
        ["Receive Invoice"]
    )

    match_completed = get_event_time(
        direct_po_events,
        [
            "Three-way Match - Successful",
            "Three-way Match - Mismatch Found"
        ]
    )

    # ========================================================
    # 6. FIND INVOICE IDs
    # ========================================================

    invoice_ids = transaction["invoice_ids"]

    if pd.isna(invoice_ids) or str(invoice_ids).strip() == "":
        invoice_list = []
    else:
        invoice_list = [
            x.strip()
            for x in str(invoice_ids).split(";")
            if x.strip()
        ]

    # ========================================================
    # 7. FIND PAYMENT AFTER MATCH
    # ========================================================

    invoice_events = event_relations[
        event_relations["object_id"].isin(invoice_list)
    ].copy()

    payment_events = invoice_events[
        invoice_events["event_type"] == "Make Payment"
    ].copy()

    # IMPORTANT:
    # Only payments occurring AFTER the three-way match
    # are considered for match-to-payment duration.

    if pd.notna(match_completed):

        payment_events_after_match = payment_events[
            payment_events["timestamp"] > match_completed
        ]

        if payment_events_after_match.empty:
            payment_made = pd.NaT
        else:
            payment_made = (
                payment_events_after_match["timestamp"]
                .min()
            )

    else:

        payment_made = pd.NaT

    # ========================================================
    # 8. START / END TIME
    # ========================================================

    timestamps = [
        pr_creation,
        pr_approval,
        po_creation,
        po_approval,
        po_sent,
        goods_received,
        invoice_received,
        match_completed,
        payment_made
    ]

    valid_timestamps = [
        timestamp
        for timestamp in timestamps
        if pd.notna(timestamp)
    ]

    if valid_timestamps:

        start_time = min(valid_timestamps)
        end_time = max(valid_timestamps)

    else:

        start_time = pd.NaT
        end_time = pd.NaT

    # ========================================================
    # 9. PROCESS DURATIONS
    # ========================================================

    total_processing_time = hours_between(
        start_time,
        end_time
    )

    pr_to_po = hours_between(
        pr_creation,
        po_creation
    )

    po_approval_delay = hours_between(
        po_creation,
        po_approval
    )

    approval_to_supplier = hours_between(
        po_approval,
        po_sent
    )

    supplier_to_goods = hours_between(
        po_sent,
        goods_received
    )

    goods_to_invoice = hours_between(
        goods_received,
        invoice_received
    )

    invoice_to_match = hours_between(
        invoice_received,
        match_completed
    )

    match_to_payment = hours_between(
        match_completed,
        payment_made
    )

    # ========================================================
    # 10. MATCH RESULT
    # ========================================================

    event_types = (
        direct_po_events["event_type"]
        .dropna()
        .unique()
    )

    successful_match = (
        "Three-way Match - Successful"
        in event_types
    )

    mismatch_found = (
        "Three-way Match - Mismatch Found"
        in event_types
    )

    if successful_match and mismatch_found:

        match_result = "Successful + Mismatch"

    elif successful_match:

        match_result = "Successful"

    elif mismatch_found:

        match_result = "Mismatch"

    else:

        match_result = "No Match Event"

    # ========================================================
    # 11. CREATE RESULT
    # ========================================================

    result = {
        "case_id": po_id,
        "po_id": po_id,

        "pr_count": transaction["pr_count"],
        "pr_ids": transaction["pr_ids"],

        "supplier_count": transaction["supplier_count"],
        "supplier_ids": transaction["supplier_ids"],

        "goods_receipt_count":
            transaction["goods_receipt_count"],

        "goods_receipt_ids":
            transaction["goods_receipt_ids"],

        "invoice_count":
            transaction["invoice_count"],

        "invoice_ids":
            transaction["invoice_ids"],

        "payment_count":
            transaction["payment_count"],

        "payment_ids":
            transaction["payment_ids"],

        "start_time":
            start_time,

        "end_time":
            end_time,

        "total_processing_time_hours":
            total_processing_time,

        "pr_to_po_hours":
            pr_to_po,

        "po_approval_hours":
            po_approval_delay,

        "approval_to_supplier_hours":
            approval_to_supplier,

        "supplier_to_goods_hours":
            supplier_to_goods,

        "goods_to_invoice_hours":
            goods_to_invoice,

        "invoice_to_match_hours":
            invoice_to_match,

        "match_to_payment_hours":
            match_to_payment,

        "rejection_count":
            rejection_count,

        "match_result":
            match_result
    }

    # VERY IMPORTANT:
    # This must remain INSIDE the for-loop.

    results.append(result)


# ============================================================
# CREATE DATAFRAME
# ============================================================

timing_features = pd.DataFrame(results)


# ============================================================
# SAVE OUTPUT
# ============================================================

timing_features.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n========================================")
print("PROCESS TIMING FEATURES CREATED")
print("========================================")

print(
    f"Procurement cases: {len(timing_features)}"
)

print(
    f"Output file: {OUTPUT_FILE}"
)


# ============================================================
# TIMESTAMP COVERAGE
# ============================================================

print("\n========================================")
print("TIMESTAMP COVERAGE")
print("========================================")

for column in [
    "start_time",
    "end_time"
]:

    missing = timing_features[column].isna().sum()

    available = (
        len(timing_features) - missing
    )

    print(
        f"{column}: "
        f"{available} available, "
        f"{missing} missing"
    )


# ============================================================
# FEATURE COVERAGE
# ============================================================

print("\n========================================")
print("FEATURE COVERAGE")
print("========================================")

feature_columns = [
    "pr_to_po_hours",
    "po_approval_hours",
    "approval_to_supplier_hours",
    "supplier_to_goods_hours",
    "goods_to_invoice_hours",
    "invoice_to_match_hours",
    "match_to_payment_hours"
]

for column in feature_columns:

    available = (
        timing_features[column]
        .notna()
        .sum()
    )

    print(
        f"{column}: "
        f"{available}/{len(timing_features)} available"
    )


# ============================================================
# NEGATIVE DURATION CHECK
# ============================================================

print("\n========================================")
print("NEGATIVE DURATION CHECK")
print("========================================")

negative_count = (
    timing_features[
        "match_to_payment_hours"
    ] < 0
).sum()

print(
    f"Negative match-to-payment durations: "
    f"{negative_count}"
)


# ============================================================
# REJECTION ANALYSIS
# ============================================================

print("\n========================================")
print("REJECTION ANALYSIS")
print("========================================")

print(
    "POs with at least one rejection: "
    f"{(timing_features['rejection_count'] > 0).sum()}"
)

print(
    "Total PR rejections detected: "
    f"{timing_features['rejection_count'].sum()}"
)


# ============================================================
# MATCH RESULTS
# ============================================================

print("\n========================================")
print("MATCH RESULTS")
print("========================================")

print(
    timing_features[
        "match_result"
    ].value_counts()
)


# ============================================================
# DURATION STATISTICS
# ============================================================

print("\n========================================")
print("DURATION STATISTICS")
print("========================================")

duration_columns = [
    "total_processing_time_hours",
    "pr_to_po_hours",
    "po_approval_hours",
    "approval_to_supplier_hours",
    "supplier_to_goods_hours",
    "goods_to_invoice_hours",
    "invoice_to_match_hours",
    "match_to_payment_hours"
]

print(
    timing_features[
        duration_columns
    ].describe()
)


# ============================================================
# SAMPLE
# ============================================================

print("\n========================================")
print("FIRST 10 RECORDS")
print("========================================")

print(
    timing_features[
        [
            "po_id",
            "pr_count",
            "pr_to_po_hours",
            "po_approval_hours",
            "approval_to_supplier_hours",
            "supplier_to_goods_hours",
            "goods_to_invoice_hours",
            "invoice_to_match_hours",
            "match_to_payment_hours",
            "rejection_count",
            "match_result"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n========================================")
print("FINAL VALIDATION")
print("========================================")

print(
    f"Expected procurement cases: "
    f"{len(transactions)}"
)

print(
    f"Generated procurement cases: "
    f"{len(timing_features)}"
)

if len(timing_features) == len(transactions):

    print("Case count validation: PASSED")

else:

    print("Case count validation: FAILED")


print("\n========================================")
print("STAGE 2.9 CORRECTION COMPLETED")
print("========================================")