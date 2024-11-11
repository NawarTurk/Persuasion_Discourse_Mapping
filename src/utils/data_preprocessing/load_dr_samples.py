import csv
import json
import os

dataset_path = os.path.join("..","dataset")
file_path = os.path.join(dataset_path, "01_raw_data", "discourse_relations", "sample_one", "PDTB3_example_paragraphs_with_labels.csv")
save_path = os.path.join(dataset_path, "02_processed_data", "dr_actual_labels_sample1.json")

def load_dr_data_from_csv():
    
    data_dic = {}
    sample_index = 1

    print("Starting to load data from CSV file...")

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):  
            if row['test_token'] == 'y':
                data_dic[sample_index] = {
                    'token_id' : row['token_id'],
                    'text': row['token'],
                    "actual_DR_level2": row['level2'],
                    "predicted_DR_level2": None,
                    "test_token": row['test_token']
                }
                sample_index += 1

    with open(save_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data_dic, jsonfile, indent=2, ensure_ascii=False)

    print(f"Data successfully saved to {save_path}")
