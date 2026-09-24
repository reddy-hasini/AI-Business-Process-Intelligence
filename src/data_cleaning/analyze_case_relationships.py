import pandas as pd


# ==========================================
# LOAD DATA
# ==========================================

events = pd.read_csv(
    "data/processed/events.csv"
)

objects = pd.read_csv(
    "data/processed/objects.csv"
)

relations = pd.read_csv(
    "data/processed/event_object_relations.csv"
)


# ==========================================
# MERGE RELATIONSHIPS WITH OBJECT TYPES
# ==========================================

relationship_data = relations.merge(
    objects[
        [
            "object_id",
            "object_type"
        ]
    ],
    on="object_id",
    how="left"
)


# ==========================================
# OBJECT TYPE → OBJECT COUNT IN RELATIONS
# ==========================================

print("=" * 60)
print("OBJECT RELATIONSHIP ANALYSIS")
print("=" * 60)

print("\nObject types represented in event relationships:")

print(
    relationship_data["object_type"]
    .value_counts()
)


# ==========================================
# SAMPLE OBJECTS
# ==========================================

print("\n" + "=" * 60)
print("SAMPLE OBJECT IDs")
print("=" * 60)

for object_type in objects["object_type"].unique():

    print(f"\n--- {object_type} ---")

    sample_ids = (
        objects[
            objects["object_type"] == object_type
        ]["object_id"]
        .head(10)
        .tolist()
    )

    print(sample_ids)


# ==========================================
# EVENTS CONNECTED TO PURCHASE REQUISITIONS
# ==========================================

print("\n" + "=" * 60)
print("PURCHASE REQUISITION EVENT EXAMPLE")
print("=" * 60)

pr_ids = objects[
    objects["object_type"] == "Purchase Requisition"
]["object_id"].head(5)

pr_events = relationship_data[
    relationship_data["object_id"].isin(pr_ids)
]

print(
    pr_events[
        [
            "event_id",
            "object_id",
            "object_type"
        ]
    ].to_string(index=False)
)


# ==========================================
# EVENTS CONNECTED TO PURCHASE ORDERS
# ==========================================

print("\n" + "=" * 60)
print("PURCHASE ORDER EVENT EXAMPLE")
print("=" * 60)

po_ids = objects[
    objects["object_type"] == "Purchase Order"
]["object_id"].head(5)

po_events = relationship_data[
    relationship_data["object_id"].isin(po_ids)
]

print(
    po_events[
        [
            "event_id",
            "object_id",
            "object_type"
        ]
    ].to_string(index=False)
)


# ==========================================
# FINAL
# ==========================================

print("\n" + "=" * 60)
print("RELATIONSHIP ANALYSIS COMPLETED")
print("=" * 60)