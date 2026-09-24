import json
import csv
import os

# ==========================================
# PATHS
# ==========================================

INPUT_FILE = "data/raw/lrms_02_p2p.json"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# LOAD DATASET
# ==========================================

print("Loading dataset...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Dataset loaded successfully!")


# ==========================================
# 1. EXTRACT EVENTS
# ==========================================

events = data.get("events", [])

event_rows = []

for event in events:

    attributes = {}

    for attribute in event.get("attributes", []):
        attributes[attribute["name"]] = attribute.get("value")

    event_rows.append({
        "event_id": event.get("id"),
        "event_type": event.get("type"),
        "timestamp": event.get("time"),
        "user": attributes.get("user"),
        "cost_center": attributes.get("cost_center")
    })


events_file = os.path.join(OUTPUT_DIR, "events.csv")

with open(events_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "event_id",
            "event_type",
            "timestamp",
            "user",
            "cost_center"
        ]
    )

    writer.writeheader()
    writer.writerows(event_rows)


print(f"Events extracted: {len(event_rows)}")
print(f"Saved to: {events_file}")


# ==========================================
# 2. EXTRACT OBJECTS
# ==========================================

objects = data.get("objects", [])

object_rows = []

for obj in objects:

    attributes = {}

    for attribute in obj.get("attributes", []):

        name = attribute.get("name")
        value = attribute.get("value")

        # Keep the latest value if an attribute appears multiple times
        attributes[name] = value

    object_rows.append({
        "object_id": obj.get("id"),
        "object_type": obj.get("type"),
        "total_amount": attributes.get("total_amount"),
        "status": attributes.get("status")
    })


objects_file = os.path.join(OUTPUT_DIR, "objects.csv")

with open(objects_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "object_id",
            "object_type",
            "total_amount",
            "status"
        ]
    )

    writer.writeheader()
    writer.writerows(object_rows)


print(f"Objects extracted: {len(object_rows)}")
print(f"Saved to: {objects_file}")


# ==========================================
# 3. EXTRACT EVENT-OBJECT RELATIONSHIPS
# ==========================================

relationship_rows = []

for event in events:

    event_id = event.get("id")

    for relationship in event.get("relationships", []):

        relationship_rows.append({
            "event_id": event_id,
            "object_id": relationship.get("objectId"),
            "qualifier": relationship.get("qualifier")
        })


relationships_file = os.path.join(
    OUTPUT_DIR,
    "event_object_relations.csv"
)

with open(
    relationships_file,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "event_id",
            "object_id",
            "qualifier"
        ]
    )

    writer.writeheader()
    writer.writerows(relationship_rows)


print(
    f"Event-object relationships extracted: "
    f"{len(relationship_rows)}"
)

print(f"Saved to: {relationships_file}")


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n========================================")
print("EXTRACTION COMPLETED")
print("========================================")

print(f"Events: {len(event_rows)}")
print(f"Objects: {len(object_rows)}")
print(f"Relationships: {len(relationship_rows)}")

print("\nOutput files:")

print("1.", events_file)
print("2.", objects_file)
print("3.", relationships_file)

print("\nStage 2.3 completed successfully!")