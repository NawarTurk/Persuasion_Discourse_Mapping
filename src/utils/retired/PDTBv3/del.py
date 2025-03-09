import json
from collections import Counter

with open('final_PDTBv3_filtered_dict.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

counter =Counter()

for key, item in data.items():
    counter[key] = len(item)

print(len(data))