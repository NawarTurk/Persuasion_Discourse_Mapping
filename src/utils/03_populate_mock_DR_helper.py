import os
import json
import random

dataset_path = os.path.join("..","..","dataset")
partial_annotated_dataset_with_text = os.path.join(dataset_path,"02_processed_data","partial_annotated_dataset_with_text.json")
DR_list = ["temporal", "contingency", "comparision", "expansion"]
output_path = os.path.join(dataset_path, "02_processed_data", "complete_mockup_DR_dataset.json")

with open(partial_annotated_dataset_with_text) as json_file:
    dataset= json.load(json_file)

for paragraphs in dataset.values():
    for para in paragraphs.values():
        para["DR"].append(random.choice(DR_list))

with open(output_path, 'w') as json_file:
    json.dump(dataset, json_file, indent=2)

