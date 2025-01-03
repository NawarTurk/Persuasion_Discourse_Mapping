import csv
import json
import os

dataset_path = os.path.join("..","dataset")
file_path = os.path.join(dataset_path, "01_raw_data", "discourse_relations", "sample_one", "PDTB3_example_paragraphs_with_labels_126instances.csv")
save_path = os.path.join(dataset_path, "02_processed_data", "discourse_relations", "DR_labeled_sample1_126instances.json")

def extract_sample1_DR_data():
    
    data_dict = {}
    sample_index = 1

    print("\nStarting to load data from CSV file...")

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):  
            if row['test_token'] == 'y':
                data_dict[sample_index] = {
                    'token_id' : row['token_id'],
                    'text': row['token'],
                    'actual_DR_level1': row['level1'].lower(),
                    "actual_DR_level2": row['level2'].lower(),
                    "predicted_DR_level2": None,
                    "test_token": row['test_token'],
                    'actual_DR_level3': row['level3'].lower()
                }
                sample_index += 1

    with open(save_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data_dict, jsonfile, indent=2, ensure_ascii=False)

    print(f"Data successfully saved to {save_path}")
