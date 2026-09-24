import pandas as pd


# ==========================================
# LOAD PROCESSED DATA
# ==========================================

events_file = "data/processed/events.csv"
objects_file = "data/processed/objects.csv"
relations_file = "data/processed/event_object_relations.csv"

events = pd.read_csv(events_file)
objects = pd.read_csv(objects_file)
relations = pd.read_csv(relations_file)


print("=" * 50)
print("DATA VALIDATION")
print("=" * 50)


# ==========================================
# 1. BASIC COUNTS
# ==========================================

print("\n--- RECORD COUNTS ---")

print("Events:", len(events))
print("Objects:", len(objects))
print("Relationships:", len(relations))


# ==========================================
# 2. EVENT TYPES
# ==========================================

print("\n--- EVENT TYPES ---")

event_types = events["event_type"].value_counts()

print(event_types)


# ==========================================
# 3. OBJECT TYPES
# ==========================================

print("\n--- OBJECT TYPES ---")

object_types = objects["object_type"].value_counts()

print(object_types)


# ==========================================
# 4. MISSING VALUES
# ==========================================

print("\n--- MISSING VALUES ---")

print("\nEvents:")
print(events.isnull().sum())

print("\nObjects:")
print(objects.isnull().sum())

print("\nRelationships:")
print(relations.isnull().sum())


# ==========================================
# 5. DUPLICATE RECORDS
# ==========================================

print("\n--- DUPLICATES ---")

print("Duplicate events:", events["event_id"].duplicated().sum())

print("Duplicate objects:", objects["object_id"].duplicated().sum())

print(
    "Duplicate relationships:",
    relations.duplicated().sum()
)


# ==========================================
# 6. TIMESTAMP VALIDATION
# ==========================================

print("\n--- TIMESTAMP VALIDATION ---")

events["timestamp"] = pd.to_datetime(
    events["timestamp"],
    errors="coerce"
)

invalid_timestamps = events["timestamp"].isna().sum()

print("Invalid timestamps:", invalid_timestamps)

print("Earliest event:", events["timestamp"].min())

print("Latest event:", events["timestamp"].max())


# ==========================================
# 7. EVENT RELATIONSHIP VALIDATION
# ==========================================

print("\n--- RELATIONSHIP VALIDATION ---")

valid_event_ids = set(events["event_id"])

valid_object_ids = set(objects["object_id"])

missing_events = ~relations["event_id"].isin(valid_event_ids)

missing_objects = ~relations["object_id"].isin(valid_object_ids)

print(
    "Relationships with missing event:",
    missing_events.sum()
)

print(
    "Relationships with missing object:",
    missing_objects.sum()
)


# ==========================================
# 8. EVENT RELATIONSHIP COUNTS
# ==========================================

print("\n--- RELATIONSHIPS PER EVENT ---")

relationships_per_event = (
    relations.groupby("event_id")
    .size()
)

print(
    relationships_per_event.describe()
)


# ==========================================
# 9. OBJECT RELATIONSHIP COUNTS
# ==========================================

print("\n--- RELATIONSHIPS PER OBJECT ---")

relationships_per_object = (
    relations.groupby("object_id")
    .size()
)

print(
    relationships_per_object.describe()
)


# ==========================================
# FINAL RESULT
# ==========================================

print("\n" + "=" * 50)
print("VALIDATION COMPLETED")
print("=" * 50)