import json
import os
from utils.helpers.pt_dr_getters import get_PT_id_by_name

dataset_path = os.path.join("..","dataset")  # improve the way we are handling the different paths
PTlabel_file_path=os.path.join(dataset_path,  "01_raw_data", "persuasion_techniques","PT_labels.txt")
articles_path=os.path.join(dataset_path,"01_raw_data", "persuasion_techniques", "articles")
output_json_path=os.path.join(dataset_path, "02_processed_data", "persuasion_techniques", "semeval_PT_annotated_dataset.json")

def extract_semeval_PT_data():
    def get_para_text(article_num, paragraph_num):
        with open(os.path.join(articles_path, f'article{article_num}.txt'), 'r', encoding='utf-8') as article:
            article_paragraphs = article.readlines()
            para_index = int(paragraph_num) - 1
            return article_paragraphs[para_index].strip()
        
    print(f"\n\nStarting extraction process...\nReading from PT label file: {PTlabel_file_path}\nArticles path: {articles_path}")
      
    partially_annotated_dataset = {}
    i = 0
    with open(PTlabel_file_path, 'r') as infile:
        for line in infile:
            article_num, paragraph_num, *PT_techniques = line.strip().split('\t')
            if PT_techniques:
                for PT in PT_techniques[0].split(','):
                    partially_annotated_dataset[i] = {
                    'article_num': int(article_num),
                    'para_num': int(paragraph_num),
                    'text': get_para_text(article_num, paragraph_num),
                    'PT_id': get_PT_id_by_name(PT),
                    'PT': PT,
                    'predicted_DR': '',
                    'parser': '',
                    'DR_id': 0,
                    ''
                    'DR': ''
                    }
                    i += 1

    with open(output_json_path, 'w', encoding= 'utf-8') as json_file:
        json.dump(partially_annotated_dataset, json_file, indent=2, ensure_ascii=False)

    print(f"\nExtraction complete. Processed {i-1} annotations.")
    print(f"Output saved to: {output_json_path}")






