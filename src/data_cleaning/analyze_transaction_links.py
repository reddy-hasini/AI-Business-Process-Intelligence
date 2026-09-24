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
# ADD OBJECT TYPE TO RELATIONSHIPS
# ==========================================

linked = relations.merge(
    objects[
        ["object_id", "object_type"]
    ],
    on="object_id",
    how="left"
)

linked = linked.merge(
    events[
        ["event_id", "event_type", "timestamp"]
    ],
    on="event_id",
    how="left"
)


# ==========================================
# MULTI-OBJECT EVENTS
# ==========================================

event_object_counts = (
    linked
    .groupby("event_id")["object_type"]
    .nunique()
)

multi_object_events = (
    event_object_counts[
        event_object_counts > 1
    ]
)

print("=" * 60)
print("MULTI-OBJECT EVENT ANALYSIS")
print("=" * 60)

print(
    "Total events:",
    len(event_object_counts)
)

print(
    "Multi-object events:",
    len(multi_object_events)
)


# ==========================================
# OBJECT TYPE COMBINATIONS
# ==========================================

print("\n" + "=" * 60)
print("OBJECT TYPE COMBINATIONS")
print("=" * 60)

for event_id in multi_object_events.index:

    event_rows = linked[
        linked["event_id"] == event_id
    ]

    event_type = event_rows[
        "event_type"
    ].iloc[0]

    object_types = sorted(
        event_rows["object_type"]
        .unique()
    )

    print(
        f"{event_type}: "
        f"{' + '.join(object_types)}"
    )


# ==========================================
# SUMMARY BY EVENT TYPE
# ==========================================

print("\n" + "=" * 60)
print("MULTI-OBJECT EVENTS BY ACTIVITY")
print("=" * 60)

multi_linked = linked[
    linked["event_id"].isin(
        multi_object_events.index
    )
]

summary = (
    multi_linked
    .groupby("event_type")["event_id"]
    .nunique()
    .sort_values(
        ascending=False
    )
)

print(summary)


# ==========================================
# SAMPLE TRANSACTION LINKS
# ==========================================

print("\n" + "=" * 60)
print("SAMPLE MULTI-OBJECT EVENTS")
print("=" * 60)

sample_ids = (
    multi_object_events
    .head(15)
    .index
)

for event_id in sample_ids:

    rows = linked[
        linked["event_id"] == event_id
    ]

    print("\nEvent:", event_id)
    print("Activity:", rows["event_type"].iloc[0])
    print("Timestamp:", rows["timestamp"].iloc[0])

    print(
        rows[
            [
                "object_id",
                "object_type"
            ]
        ].to_string(index=False)
    )


print("\n" + "=" * 60)
print("TRANSACTION LINK ANALYSIS COMPLETED")
print("=" * 60)