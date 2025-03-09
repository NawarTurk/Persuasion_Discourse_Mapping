import json

# Load the first JSON file with utf-8 encoding
with open('semeval_PT_dataset_3.json', 'r', encoding='utf-8') as jsonfile1:
    data3 = json.load(jsonfile1)

# Load the second JSON file with utf-8 encoding
with open('semeval_PT_dataset_4.json', 'r', encoding='utf-8') as jsonfile2:
    data4 = json.load(jsonfile2)

# Load the second JSON file with utf-8 encoding
with open('semeval_PT_dataset_5.json', 'r', encoding='utf-8') as jsonfile2:
    data5 = json.load(jsonfile2)

# Load the second JSON file with utf-8 encoding
with open('semeval_PT_dataset_6.json', 'r', encoding='utf-8') as jsonfile2:
    data6 = json.load(jsonfile2)

# Load the second JSON file with utf-8 encoding
with open('semeval_PT_dataset_7.json', 'r', encoding='utf-8') as jsonfile2:
    data7 = json.load(jsonfile2)


# Combine the two datasets (assuming they are lists of dictionaries)
combined_data = {**data3, **data4, **data5, **data6, **data7}

filtered_data = {
    key: entry for key, entry in combined_data.items() if len(entry['text'].split()) >=4
    }

# Save the combined dataset to a new JSON file with utf-8 encoding
with open('combinedataset3and4567.json', 'w', encoding='utf-8') as outfile:
    json.dump(filtered_data, outfile, indent=2, ensure_ascii=False)

print(f"Combined dataset contains {len(filtered_data)} entries.")




print(len(filtered_data))

