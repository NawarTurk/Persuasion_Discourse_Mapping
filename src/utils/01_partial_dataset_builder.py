import os
import json

dataset_path = os.path.join("..", "..","dataset")
articles_path=os.path.join(dataset_path,"01_raw_data","articles")
PRlabel_file_path=os.path.join(dataset_path, "01_raw_data", "PR_labels.txt")
output_json_path=os.path.join(dataset_path, "02_processed_data", "partial_annotated_dataset.json")

partial_annotated_dataset ={}
with open(PRlabel_file_path, 'r') as infile:
    for line in infile:
        article_num, paragraph_num, *PR_techniques = line.strip().split('\t')
        if PR_techniques:
            if article_num not in partial_annotated_dataset:
                partial_annotated_dataset[article_num] = {}
            partial_annotated_dataset[article_num][paragraph_num] = {}
            partial_annotated_dataset[article_num][paragraph_num]['text'] = ''
            partial_annotated_dataset[article_num][paragraph_num]['PT'] = PR_techniques[0].split(',')
            partial_annotated_dataset[article_num][paragraph_num]['DR'] = []

with open(output_json_path, 'w') as json_file:
    json.dump(partial_annotated_dataset, json_file, indent=4)






