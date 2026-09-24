import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RELATIONS_FILE = "data/processed/event_object_relations.csv"
EVENTS_FILE = "data/processed/events.csv"
OBJECTS_FILE = "data/processed/objects.csv"

OUTPUT_FILE = "data/processed/procurement_cases.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading data...")

relations = pd.read_csv(RELATIONS_FILE)
events = pd.read_csv(EVENTS_FILE)
objects = pd.read_csv(OBJECTS_FILE)

print(f"Relations loaded: {len(relations)}")
print(f"Events loaded: {len(events)}")
print(f"Objects loaded: {len(objects)}")


# ============================================================
# PREPARE RELATIONSHIPS
# ============================================================

# Add object type information to every relationship
relations_with_objects = relations.merge(
    objects[["object_id", "object_type"]],
    on="object_id",
    how="left"
)

# Add event information
event_relations = relations_with_objects.merge(
    events,
    on="event_id",
    how="left"
)

print("\nMerged event-relationship data:")
print(f"Rows: {len(event_relations)}")


# ============================================================
# IDENTIFY PURCHASE ORDERS
# ============================================================

po_objects = objects[
    objects["object_type"] == "Purchase Order"
]["object_id"].unique()

print(f"\nPurchase Orders found: {len(po_objects)}")


# ============================================================
# CREATE PO-CENTERED TRANSACTION MAP
# ============================================================

procurement_cases = []


for po_id in po_objects:

    # --------------------------------------------------------
    # Find all events directly connected to this PO
    # --------------------------------------------------------

    po_rows = event_relations[
        event_relations["object_id"] == po_id
    ]

    po_event_ids = (
        po_rows["event_id"]
        .dropna()
        .unique()
    )

    # --------------------------------------------------------
    # Get ALL objects connected through those events
    # --------------------------------------------------------

    related_rows = event_relations[
        event_relations["event_id"].isin(po_event_ids)
    ]

    # --------------------------------------------------------
    # Purchase Requisitions
    # --------------------------------------------------------

    pr_ids = sorted(
        related_rows.loc[
            related_rows["object_type"] == "Purchase Requisition",
            "object_id"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    # --------------------------------------------------------
    # Suppliers
    # --------------------------------------------------------

    supplier_ids = sorted(
        related_rows.loc[
            related_rows["object_type"] == "Supplier",
            "object_id"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    # --------------------------------------------------------
    # Goods Receipts
    # --------------------------------------------------------

    goods_receipt_ids = sorted(
        related_rows.loc[
            related_rows["object_type"] == "Goods Receipt",
            "object_id"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    # --------------------------------------------------------
    # Invoices
    # --------------------------------------------------------

    invoice_ids = sorted(
        related_rows.loc[
            related_rows["object_type"] == "Invoice",
            "object_id"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    # --------------------------------------------------------
    # Payments
    # --------------------------------------------------------

    payment_ids = []

    for invoice_id in invoice_ids:

        invoice_rows = event_relations[
            event_relations["object_id"] == invoice_id
        ]

        invoice_event_ids = (
            invoice_rows["event_id"]
            .dropna()
            .unique()
        )

        payment_rows = event_relations[
            (event_relations["event_id"].isin(invoice_event_ids))
            &
            (event_relations["object_type"] == "Payment")
        ]

        payment_ids.extend(
            payment_rows["object_id"]
            .dropna()
            .unique()
            .tolist()
        )

    payment_ids = sorted(set(payment_ids))

    # --------------------------------------------------------
    # Match Result
    # --------------------------------------------------------

    successful_match = (
        "Three-way Match - Successful"
        in related_rows["event_type"].dropna().values
    )

    mismatch_found = (
        "Three-way Match - Mismatch Found"
        in related_rows["event_type"].dropna().values
    )

    if successful_match and mismatch_found:
        match_result = "Successful + Mismatch"
    elif successful_match:
        match_result = "Successful"
    elif mismatch_found:
        match_result = "Mismatch"
    else:
        match_result = "No Match Event"

    # --------------------------------------------------------
    # Create transaction record
    # --------------------------------------------------------

    procurement_cases.append({

        "case_id": po_id,

        "po_id": po_id,

        "pr_count": len(pr_ids),
        "pr_ids": ";".join(pr_ids),

        "supplier_count": len(supplier_ids),
        "supplier_ids": ";".join(supplier_ids),

        "goods_receipt_count": len(goods_receipt_ids),
        "goods_receipt_ids": ";".join(goods_receipt_ids),

        "invoice_count": len(invoice_ids),
        "invoice_ids": ";".join(invoice_ids),

        "payment_count": len(payment_ids),
        "payment_ids": ";".join(payment_ids),

        "match_result": match_result
    })


# ============================================================
# CREATE DATAFRAME
# ============================================================

procurement_cases = pd.DataFrame(
    procurement_cases
)


# ============================================================
# SAVE OUTPUT
# ============================================================

procurement_cases.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n========================================")
print("PO TRANSACTION MAP CREATED")
print("========================================")

print(f"Purchase Orders mapped: {len(procurement_cases)}")

print(f"\nOutput file:")
print(OUTPUT_FILE)

print("\nColumns:")
for column in procurement_cases.columns:
    print(f"- {column}")


# ============================================================
# SAMPLE DATA
# ============================================================

print("\nFirst 10 procurement cases:")

print(
    procurement_cases.head(10).to_string(index=False)
)


# ============================================================
# PR DISTRIBUTION
# ============================================================

print("\nPR count distribution:")

print(
    procurement_cases[
        "pr_count"
    ]
    .value_counts()
    .sort_index()
)


# ============================================================
# MATCH DISTRIBUTION
# ============================================================

print("\nMatch result distribution:")

print(
    procurement_cases[
        "match_result"
    ]
    .value_counts()
)


# ============================================================
# VALIDATION
# ============================================================

print("\n========================================")
print("VALIDATION")
print("========================================")

print(
    f"Rows in output: {len(procurement_cases)}"
)

print(
    f"Unique PO IDs: {procurement_cases['po_id'].nunique()}"
)

print(
    f"POs with PRs: "
    f"{(procurement_cases['pr_count'] > 0).sum()}"
)

print(
    f"POs with Supplier: "
    f"{(procurement_cases['supplier_count'] > 0).sum()}"
)

print(
    f"POs with Goods Receipt: "
    f"{(procurement_cases['goods_receipt_count'] > 0).sum()}"
)

print(
    f"POs with Invoice: "
    f"{(procurement_cases['invoice_count'] > 0).sum()}"
)

print(
    f"POs with Payment: "
    f"{(procurement_cases['payment_count'] > 0).sum()}"
)

print("\n========================================")
print("STAGE 2.8 COMPLETED")
print("========================================")