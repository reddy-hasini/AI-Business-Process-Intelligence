import json

file_path = "data/raw/lrms_02_p2p.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Dataset loaded successfully!")

print("\n========== TOP-LEVEL STRUCTURE ==========")

for key, value in data.items():

    print(f"\n{key}")
    print("Type:", type(value).__name__)

    if isinstance(value, list):
        print("Number of records:", len(value))

        if len(value) > 0:
            print("First record:")
            print(value[0])

    elif isinstance(value, dict):
        print("Number of keys:", len(value))
        print("Sample:")
        print(list(value.items())[:2])