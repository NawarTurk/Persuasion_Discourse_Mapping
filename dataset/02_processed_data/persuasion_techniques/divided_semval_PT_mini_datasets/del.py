import json
from collections import Counter

with open('PT_dataset_2.json', 'r') as f:
    data = json.load(f)

with open('PT_dataset_1.json', 'r') as f:
    data2 = json.load(f)


print(len(data))
print(2160+2155)

counter = Counter()
for value in data.values():
    counter[value['PT']] +=1

for value in data2.values():
    counter[value['PT']] +=1

counter = dict(sorted(counter.items()))

print(json.dumps(counter, indent=2))