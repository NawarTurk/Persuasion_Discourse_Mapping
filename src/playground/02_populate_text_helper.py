import json
import os

dataset_path = os.path.join('..', '..', 'dataset')
articles_path = os.path.join(dataset_path, "01_raw_data", 'articles')
partial_annotated_dataset_json_path = os.path.join(dataset_path,"02_processed_data", 'partial_annotated_dataset.json')
output_json_path = os.path.join(dataset_path, "02_processed_data", 'partial_annotated_dataset_with_text.json')


with open(partial_annotated_dataset_json_path, 'r') as json_file:
    dataset= json.load(json_file)


def update_dataset_with_text(article_num, paragraph_details):
    article_path = os.path.join(articles_path,f'article{article_num}.txt')
    with open(article_path, 'r') as file:
        paragrpghs = file.readlines()
        for paragraph_num, details in paragraph_details.items():
            paragraph_index = int(paragraph_num) - 1
            if paragraph_index < len(paragrpghs):
                details['text'] = paragrpghs[paragraph_index].strip()
            else:
                print('paragraph index out of range')  # this should not print at all


with open(partial_annotated_dataset_json_path, 'r') as json_file:
    dataset= json.load(json_file)

for article_num, paragraph_details in dataset.items():
    update_dataset_with_text(article_num, paragraph_details)

with open(output_json_path, 'w') as json_file:
    json.dump(dataset, json_file, indent=2)
