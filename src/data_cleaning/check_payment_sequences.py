import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RELATIONS_FILE = "data/processed/event_object_relations.csv"
EVENTS_FILE = "data/processed/events.csv"
OBJECTS_FILE = "data/processed/objects.csv"
TIMING_FILE = "data/processed/procurement_timing_features.csv"

# ============================================================
# LOAD DATA
# ============================================================

print("Loading data...")

relations = pd.read_csv(RELATIONS_FILE)
events = pd.read_csv(EVENTS_FILE)
objects = pd.read_csv(OBJECTS_FILE)
timing = pd.read_csv(TIMING_FILE)

print(f"Relations: {len(relations)}")
print(f"Events: {len(events)}")
print(f"Objects: {len(objects)}")
print(f"Timing records: {len(timing)}")


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


# ============================================================
# FIND NEGATIVE PAYMENT CASES
# ============================================================

negative_cases = timing[
    timing["match_to_payment_hours"] < 0
].copy()

print("\n========================================")
print("NEGATIVE PAYMENT CASES")
print("========================================")

print(
    f"Cases with negative duration: "
    f"{len(negative_cases)}"
)

print(
    negative_cases[
        [
            "po_id",
            "invoice_ids",
            "match_to_payment_hours"
        ]
    ].to_string(index=False)
)


# ============================================================
# INSPECT EACH INVALID PO
# ============================================================

print("\n========================================")
print("EVENT SEQUENCES")
print("========================================")


for _, case in negative_cases.iterrows():

    po_id = case["po_id"]

    print("\n----------------------------------------")
    print(f"PO: {po_id}")
    print("----------------------------------------")

    # --------------------------------------------------------
    # Find events directly connected to PO
    # --------------------------------------------------------

    po_rows = event_relations[
        event_relations["object_id"] == po_id
    ]

    po_event_ids = (
        po_rows["event_id"]
        .dropna()
        .unique()
    )

    po_events = event_relations[
        event_relations["event_id"].isin(po_event_ids)
    ].copy()

    # --------------------------------------------------------
    # Show match events
    # --------------------------------------------------------

    match_events = po_events[
        po_events["event_type"].isin(
            [
                "Three-way Match - Successful",
                "Three-way Match - Mismatch Found"
            ]
        )
    ][
        [
            "event_id",
            "event_type",
            "timestamp",
            "object_id",
            "object_type"
        ]
    ].drop_duplicates()

    print("\nMATCH EVENTS:")

    if match_events.empty:
        print("No match events found.")
    else:
        print(
            match_events
            .sort_values("timestamp")
            .to_string(index=False)
        )

    # --------------------------------------------------------
    # Get invoice IDs
    # --------------------------------------------------------

    invoice_ids = (
        po_events.loc[
            po_events["object_type"] == "Invoice",
            "object_id"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    print("\nINVOICES:")
    print(invoice_ids)

    # --------------------------------------------------------
    # Find payment events through invoices
    # --------------------------------------------------------

    invoice_events = event_relations[
        event_relations["object_id"].isin(invoice_ids)
    ]

    payment_events = invoice_events[
        invoice_events["event_type"] == "Make Payment"
    ][
        [
            "event_id",
            "event_type",
            "timestamp",
            "object_id",
            "object_type"
        ]
    ].drop_duplicates()

    print("\nPAYMENT EVENTS:")

    if payment_events.empty:
        print("No payment events found.")
    else:
        print(
            payment_events
            .sort_values("timestamp")
            .to_string(index=False)
        )

    # --------------------------------------------------------
    # Show all transaction events chronologically
    # --------------------------------------------------------

    print("\nALL PO-RELATED EVENTS:")

    all_events = po_events[
        [
            "event_id",
            "event_type",
            "timestamp",
            "object_id",
            "object_type"
        ]
    ].drop_duplicates()

    print(
        all_events
        .sort_values("timestamp")
        .to_string(index=False)
    )


print("\n========================================")
print("PAYMENT SEQUENCE CHECK COMPLETED")
print("========================================")