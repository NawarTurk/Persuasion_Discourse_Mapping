import json
from collections import Counter

# Load JSON files
with open('PT_dataset_1.json', 'r') as f:
    data1 = json.load(f)

with open('PT_dataset_2.json', 'r') as f:
    data2 = json.load(f)

with open('all.json', 'r') as f:
    data3 = json.load(f)

print("Length of data1:", len(data1))
print("Length of data2:", len(data2))
print("Length of data3:", len(data3))

# Merge dictionaries (be cautious of overlapping keys)
data = {**data1, **data2}

print(len(data))

# Count 'PT' occurrences in data and data3
counter = Counter()
counter3 = Counter()

for value in data.values():
    if 'PT' in value:
        counter[value['PT']] += 1

for value in data3.values():
    if 'PT' in value:
        counter3[value['PT']] += 1

# Sort and convert to dictionaries
counter = dict(sorted(counter.items(), key= lambda item: item[1], reverse=True))
counter3 = dict(sorted(counter3.items(), key = lambda item: item[1], reverse=True))

# Save counters locally
with open('counter.json', 'w') as f:
    json.dump(counter, f, indent=4)

with open('counter3.json', 'w') as f:
    json.dump(counter3, f, indent=4)

print("Counters saved successfully as 'counter.json' and 'counter3.json'")
