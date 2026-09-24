import pandas as pd
import os


# ==========================================
# PATHS
# ==========================================

EVENTS_FILE = "data/processed/events.csv"
OBJECTS_FILE = "data/processed/objects.csv"
RELATIONS_FILE = "data/processed/event_object_relations.csv"

OUTPUT_DIR = "data/processed"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "canonical_event_log.csv"
)


# ==========================================
# LOAD DATA
# ==========================================

print("Loading processed datasets...")

events = pd.read_csv(EVENTS_FILE)
objects = pd.read_csv(OBJECTS_FILE)
relations = pd.read_csv(RELATIONS_FILE)

print("Datasets loaded successfully.")


# ==========================================
# MERGE EVENTS WITH RELATIONSHIPS
# ==========================================

event_log = relations.merge(
    events,
    on="event_id",
    how="left"
)


# ==========================================
# ADD OBJECT INFORMATION
# ==========================================

event_log = event_log.merge(
    objects[
        [
            "object_id",
            "object_type",
            "total_amount",
            "status"
        ]
    ],
    on="object_id",
    how="left"
)


# ==========================================
# CONVERT TIMESTAMP
# ==========================================

event_log["timestamp"] = pd.to_datetime(
    event_log["timestamp"],
    errors="coerce",
    utc=True
)


# ==========================================
# SORT EVENTS
# ==========================================

event_log = event_log.sort_values(
    by=["timestamp", "event_id"]
).reset_index(drop=True)


# ==========================================
# SELECT IMPORTANT COLUMNS
# ==========================================

event_log = event_log[
    [
        "event_id",
        "event_type",
        "timestamp",
        "user",
        "cost_center",
        "object_id",
        "object_type",
        "total_amount",
        "status",
        "qualifier"
    ]
]


# ==========================================
# SAVE
# ==========================================

event_log.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# SUMMARY
# ==========================================

print("\n" + "=" * 60)
print("CANONICAL EVENT LOG CREATED")
print("=" * 60)

print("Rows:", len(event_log))
print("Columns:", len(event_log.columns))

print("\nColumns:")
for column in event_log.columns:
    print("-", column)

print("\nSaved to:")
print(OUTPUT_FILE)

print("\nStage 2.6 completed successfully!")