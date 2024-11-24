import os
import json
import random
from utils.pt_dr_getters import DR_relations_level2, get_DR_relation_by_id


dataset_path = os.path.join("..","dataset")
partial_annotated_dataset_with_text = os.path.join(dataset_path, "02_processed_data", "persuasion_techniques", "semeval_PT_annotated_dataset.json")
output_path = os.path.join(dataset_path, "mock_data", "complete_dataset_with_mock_DR.json")

def populate_mock_DR():
    print("\n\nStarting to populate mock discourse relations into the dataset...")
    with open(partial_annotated_dataset_with_text) as json_file:
        dataset= json.load(json_file)

    for sample in dataset.values():
      DR_id = random.randint(1, len(DR_relations_level2))
      sample['DR_id'] = DR_id
      sample['DR'] = get_DR_relation_by_id(DR_id)

    with open(output_path, 'w') as json_file:
        json.dump(dataset, json_file, indent=2)

    print(f"Mock discourse relations populated and saved to: {output_path}\n\n")



