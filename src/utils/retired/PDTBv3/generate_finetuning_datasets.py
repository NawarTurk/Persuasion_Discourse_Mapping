import os
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Get the absolute path to the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
outputpath = os.path.join(script_dir, 'output.json')
# Construct the path to the 'gold' directory
gold_dir = os.path.join(script_dir, 'gold')

PDTBv3_dict = {}

# Iterate through each subdirectory in 'gold'
for subdir in os.listdir(gold_dir):
    subdir_path = os.path.join(gold_dir, subdir)

    # Check if the current path is a directory
    if os.path.isdir(subdir_path):
  
        files = os.listdir(subdir_path)
        files.sort()  # Sorts the list of filenames alphabetically

        # Print the sorted filenames
        for wsj_file in files:
            wsj_gold_file_path = os.path.join(subdir_path, wsj_file)
            gold_line_numb = 1
            try:
                with open(wsj_gold_file_path, 'r') as gold_file:
                    for line in gold_file:
                        fields = line.strip().split('|')

                        # DR relations
                        relation_type = fields[0]
                        DR_relations = fields[8]
                        DR_levels = DR_relations.split('.')
                        DR_level1 = DR_levels[0] if DR_levels else ''
                        DR_level2 = DR_levels[1] if len(DR_levels) > 1 else ''
                        DR_level3 = DR_levels[2] if len(DR_levels) > 2 else ''
                        second_Dr_relations = fields[9] #####
                        
                        # first argument
                        spanList_1st_arg = fields[14]
                        spanList_1st_arg_supp = fields[13]
                        spanList_1st_arg_feat = fields[19]

                        # second argument
                        spanList_2nd_arg = fields[20]
                        spanList_2nd_arg_supp = fields[26]
                        spanList_2nd_arg_feat = fields[25]

                        # connectives
                        fist_connective = fields[7]  # while
                        spanlist_conneective_feat = fields[6]
                        # spanList_explicit_connective = fields[1]  # While
                        # spanList_connective_other = fields[31]
                        second_connective = fields[10]

                        PDTBv3_dict[f'{subdir}.{wsj_file}.{gold_line_numb}'] = {
                            'folder': subdir,
                            'file': wsj_file,
                            'gold_line_number': gold_line_numb,
                            'relation_type': relation_type,
                            'DR_relations': DR_relations,
                            'actual_DR_level1': DR_level1,
                            'actual_DR_level2': DR_level2,
                            'actual_DR_level3': DR_level3,
                            'second_Dr_relations': second_Dr_relations,
                            'spanList_1st_arg': spanList_1st_arg,
                            'spanList_1st_arg_supp': spanList_1st_arg_supp,
                            'spanList_1st_arg_feat': spanList_1st_arg_feat,
                            'spanList_2nd_arg': spanList_2nd_arg,
                            'spanList_2nd_arg_supp': spanList_2nd_arg_supp,
                            'spanList_2nd_arg_feat': spanList_2nd_arg_feat,
                            'fist_connective': fist_connective,
                            'spanlist_connective_feat': spanlist_conneective_feat,
                            'connective_feat': '',
                            'first_connective_from_other': '',
                            'second_connective': second_connective,
                            'first_arg': '',
                            'second_arg': '',
                            'text': '',
                            'predicted_DR_level1': '',
                            'predicted_DR_level2': '',
                            'predicted_DR_level3': '',
                            'wsj_file': wsj_file
                        }

                        gold_line_numb += 1          
            except:
                print('error', wsj_file)




test_set = ('wsj_0010','wsj_0031','wsj_2343','wsj_1208','wsj_1208','wsj_2402','wsj_0089','wsj_0010','wsj_0010','wsj_0024','wsj_0039','wsj_0022','wsj_0019','wsj_0300','wsj_130','wsj_1803','wsj_0571','wsj_0142','wsj_0174','wsj_1803',
            'wsj_0118','wsj_0041','wsj_0089','wsj_2428','wsj_1917','wsj_2384','wsj_0245','wsj_1822','wsj_1824','wsj_0359','wsj_0616','wsj_2306','wsj_0359','wsj_2047','wsj_1866','wsj_0675','wsj_0351','wsj_1560','wsj_0976',
            'wsj_0909','wsj_0909','wsj_1397','wsj_1874','wsj_1394','wsj_0224','wsj_2118','wsj_0238','wsj_0036','wsj_0443','wsj_0118','wsj_0018','wsj_0560','wsj_0367','wsj_1600','wsj_0349','wsj_0975',
            'wsj_1646','wsj_0035','wsj_0322','wsj_2089','wsj_0080','wsj_2089','wsj_0984','wsj_0553','wsj_0089','wsj_0629','wsj_0115','wsj_1066','wsj_0956','wsj_0742','wsj_2431','wsj_0018','wsj_0022','wsj_0359','wsj_0524','wsj_0013','wsj_0359',
            'wsj_2417','wsj_0305','wsj_1574','wsj_0374','wsj_2365','wsj_0359','wsj_0333','wsj_0231','wsj_2232','wsj_2230','wsj_0128','wsj_1849','wsj_1831','wsj_0041','wsj_0304','wsj_1574','wsj_2407','wsj_2407','wsj_0331','wsj_2418','wsj_0936','wsj_0445',
            'wsj_1103','wsj_1469','wsj_0207','wsj_0569','wsj_2144','wsj_0022','wsj_0305','wsj_0911','wsj_0349','wsj_0003','wsj_2431','wsj_2451','wsj_0804','wsj_2443','wsj_0293','wsj_0120','wsj_0209','wsj_0209','wsj_0589','wsj_0118','wsj_1128','wsj_0118','wsj_0240','wsj_0300','wsj_1646','wsj_0321'
            )

PDTBv3_filtered_dict = {}
for key, instance in PDTBv3_dict.items():
    if (';' not in instance['spanList_1st_arg'] and \
        ';' not in instance['spanList_2nd_arg'] and \
        instance['relation_type'] in ['Explicit', 'Implicit'] and \
        instance['second_Dr_relations'] == '' and \
        instance['spanList_1st_arg_supp']  == '' and \
        instance['spanList_1st_arg_feat'] == '' and \
        instance['spanList_2nd_arg_supp']  == '' and \
        instance['spanList_2nd_arg_feat'] == '' and \
        instance['second_connective'] == '' and \
        instance['spanlist_connective_feat'] != '') and\
        instance['wsj_file'] not in test_set:    

            raw_path = os.path.join(script_dir, 'raw', instance['folder'], instance['file'])

            try:
                with open(raw_path, 'r') as raw_file:
                    raw_text = raw_file.read()

                    start1, end1 = map(int, instance['spanList_1st_arg'].split('..'))
                    start2, end2 = map(int, instance['spanList_2nd_arg'].split('..'))
                    first_arg = raw_text[start1:end1].strip()
                    second_arg = raw_text[start2:end2].strip()
                    instance['first_arg'] = first_arg
                    instance['second_arg'] = second_arg
                    instance['text'] = raw_text[min(start1, start2): max(end1, end2)].strip()

                    if instance['spanlist_connective_feat']:
                            if ';' not in instance['spanlist_connective_feat']:
                                start11, end11 = map(int, instance['spanlist_connective_feat'].split('..'))
                                instance['connective_feat'] = raw_text[start11:end11]
                                 
                    if 17 < len(instance['text']) < 1000 and (len(first_arg) + len(second_arg)) >= 0.7 * len(instance['text']):
                        PDTBv3_filtered_dict[key] = instance
            except:
                print('err', raw_path)
                continue

with open('PT_dataset_1.json', 'r', encoding='utf-8') as jsonfile:
    pt_data = json.load(jsonfile)


pt_text = [entry['text'] for entry in pt_data.values()]
PDTBv3_filtered_text = [entry['text'] for entry in PDTBv3_filtered_dict.values()]
PDTBv3_filtered_keys = list(PDTBv3_filtered_dict.keys())

# model = SentenceTransformer('paraphrase-distilroberta-base-v1')
model = SentenceTransformer('all-MiniLM-L6-v2')
pt_embeddings = model.encode(pt_text)
PDTBv3_filtered_embeddings = model.encode(PDTBv3_filtered_text)
similarity_matrix = cosine_similarity(pt_embeddings, PDTBv3_filtered_embeddings)

top_k=500
selected_dr_keys = set()
used_similarities = []
final_PDTBv3_filtered_dict = {}
for pt_index, similarities in enumerate(similarity_matrix):
    top_k_indices = np.argsort((similarities))[-top_k:]
    used_similarities.extend([similarities[key] for key in top_k_indices])
    for dr_index in top_k_indices:
        selected_dr_keys.add(PDTBv3_filtered_keys[dr_index])

final_PDTBv3_filtered_dict = {key: PDTBv3_filtered_dict[key] for key in selected_dr_keys}

finetuning_dataset = {}
for key, value in final_PDTBv3_filtered_dict.items():
    dr_level2 = value['actual_DR_level2']
    if dr_level2 not in finetuning_dataset:
        finetuning_dataset[dr_level2] = []
    finetuning_dataset[dr_level2].append({key: value})

# Cap the number of instances per DR level to 20 ?
for dr_level, instances in finetuning_dataset.items():
    finetuning_dataset[dr_level] = instances[:36]

with open('filtered_PDTB_dataset.json', 'w') as jsonfile:
    json.dump(finetuning_dataset, jsonfile, indent=2)
with open('filtered_PDTB_dataset.json', 'w') as jsonfile:
    json.dump(finetuning_dataset, jsonfile, indent=2)

print('final filtered', len(final_PDTBv3_filtered_dict))
print(f'max: {max(used_similarities):.4f}')
print(f'avg: {np.mean(used_similarities):.4f}')
print(f'std: {np.std(used_similarities):.4}')

prompts_files = os.listdir('.') 
txt_files = [file for file in prompts_files if file.endswith('.txt')]

for prompt_file in txt_files: 
    prompt_file
    with open(f'{prompt_file}', 'r', encoding= 'utf-8') as f:
        prompt_template = f.read()
    
    data=[]
    for dr_level2, instances in finetuning_dataset.items():
        for instance in instances:
            key, value = list(instance.items())[0]
            text = value['text']
            prompt_with_text = prompt_template.format(paragraph = text)
            data.append({"Input": prompt_with_text, "Output": value["actual_DR_level2"]})

    finetuning_df = pd.DataFrame(data)

    finetuning_df.to_excel(f'finetuning_dataset_{prompt_file}.xlsx', index=False)


with open('final_PDTBv3_filtered_dict.json', 'w') as jsonfile:
    json.dump(final_PDTBv3_filtered_dict, jsonfile, indent=2)

