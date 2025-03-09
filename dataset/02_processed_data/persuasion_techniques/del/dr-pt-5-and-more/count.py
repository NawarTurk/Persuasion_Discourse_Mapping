import json
from collections import Counter

# Load data from target.json
with open("targetHere.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Count occurrences of PT and DR
pt_counts = Counter(item["PT"] for item in data.values())
dr_counts = Counter(item["DR"] for item in data.values())

# Prepare the output dictionary
output_data = {
    "PT_Counts": dict(pt_counts),
    "DR_Counts": dict(dr_counts)
}

# Save the counts to a new JSON file
output_filename = "pt_dr_countsHERE.json"
with open(output_filename, "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, indent=4, ensure_ascii=False)

print(f"Counts saved to {output_filename}")
