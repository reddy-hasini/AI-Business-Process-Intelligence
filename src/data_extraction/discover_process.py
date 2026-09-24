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
# 1. ALL EVENT TYPES
# ==========================================

print("=" * 60)
print("EVENT TYPES")
print("=" * 60)

event_counts = (
    events["event_type"]
    .value_counts()
    .sort_index()
)

print(event_counts)


# ==========================================
# 2. ALL OBJECT TYPES
# ==========================================

print("\n" + "=" * 60)
print("OBJECT TYPES")
print("=" * 60)

object_counts = (
    objects["object_type"]
    .value_counts()
    .sort_index()
)

print(object_counts)


# ==========================================
# 3. EVENT → OBJECT CONNECTIONS
# ==========================================

print("\n" + "=" * 60)
print("EVENT → OBJECT TYPE CONNECTIONS")
print("=" * 60)

event_object = relations.merge(
    events[["event_id", "event_type"]],
    on="event_id",
    how="left"
)

event_object = event_object.merge(
    objects[["object_id", "object_type"]],
    on="object_id",
    how="left"
)

connection_counts = (
    event_object[
        ["event_type", "object_type"]
    ]
    .value_counts()
    .sort_index()
)

print(connection_counts)


# ==========================================
# 4. EVENTS PER OBJECT TYPE
# ==========================================

print("\n" + "=" * 60)
print("NUMBER OF EVENTS CONNECTED TO EACH OBJECT TYPE")
print("=" * 60)

events_per_object_type = (
    event_object
    .groupby("object_type")
    .size()
    .sort_values(ascending=False)
)

print(events_per_object_type)


# ==========================================
# 5. ACTIVITIES PER OBJECT TYPE
# ==========================================

print("\n" + "=" * 60)
print("ACTIVITIES ASSOCIATED WITH EACH OBJECT TYPE")
print("=" * 60)

activities_by_object = (
    event_object
    .groupby("object_type")["event_type"]
    .unique()
)

for object_type, activities in activities_by_object.items():

    print(f"\n{object_type}:")

    for activity in sorted(activities):
        print(f"  - {activity}")


# ==========================================
# 6. ACTIVITY FREQUENCY
# ==========================================

print("\n" + "=" * 60)
print("ACTIVITY FREQUENCY")
print("=" * 60)

activity_frequency = (
    events["event_type"]
    .value_counts()
)

print(activity_frequency)


# ==========================================
# 7. RELATIONSHIPS BY QUALIFIER
# ==========================================

print("\n" + "=" * 60)
print("RELATIONSHIP QUALIFIERS")
print("=" * 60)

print(
    relations["qualifier"]
    .value_counts(dropna=False)
)


# ==========================================
# FINAL MESSAGE
# ==========================================

print("\n" + "=" * 60)
print("PROCESS DISCOVERY COMPLETED")
print("=" * 60)