import os
import json
from collections import Counter
from utils.helpers.pt_dr_getters import get_level2_DR_id_by_name

def pool_data_and_log_results():
    direct_path = os.path.join('../', 'results', "stage2_DR_parsing_PT_annotated_semeval_datasets", "02_hallucination_removed")
    report_path = os.path.join('../', 'results', "stage2_DR_parsing_PT_annotated_semeval_datasets", "data_pooling_summary.txt")
    output_path = os.path.join('../', 'results', "stage2_DR_parsing_PT_annotated_semeval_datasets", "03_pooled_datasets")
    f1_average_path = os.path.join('../', 'results', 'stage1_eval_initial_DR_prompts_126instances', 'summary_report', 'average_f1_scores_level2_per_parser.json')

    with open(f1_average_path, 'r', encoding='utf-8') as f:
        f1_average_scores = json.load(f)
    
    
    json_files =[file for file in os.listdir(direct_path) if file.endswith('.json')]
    datasets = []
    files_numb = len(json_files)

    with open (report_path, 'w') as file:
        pass

    for json_file in json_files:
        file_path = os.path.join(direct_path, json_file)
        parser_key = json_file.replace("PT_dataset_A_", "").replace(".json", "")
        with open(file_path, 'r', encoding='utf-8') as f:
            datasets.append({
                "parser_key": parser_key,
                "data": json.load(f)
                })

    k = 0
    f1_weighted_dataset = {}  # Weighted F1 score-based dataset
    is_weighted_f1_calculated = False

    for i in range(2, files_numb+1):
        dataset = {}  # Agreement-based dataset
        k = k + 1
        for key, value in datasets[0]['data'].items():
            dr_values = [
                (dataset['data'][key]['DR'], dataset['parser_key']) for dataset in datasets
                ]
            dr_counter = Counter([dr for dr, _ in dr_values])  # Ignore parser_key in the Counter
            most_common_dr, most_common_count = dr_counter.most_common(1)[0]

            if not is_weighted_f1_calculated:
                # Calculate weighted F1 scores for each DR
                weighted_score = {}
                for dr_value in dr_values:
                    dr = dr_value[0]   
                    # Skip 'NA' values
                    if dr == 'None' or dr == 'NA':
                        continue
                    print('dr', dr)
                    dr_id = str(get_level2_DR_id_by_name(dr))
                    parser_key = dr_value[1]
                    print('parser key', parser_key)
                    print('id', dr_id)
                    print("____")
                    f1_score = round(f1_average_scores[parser_key][dr_id]['average_f1_score'],2)
                    weighted_score[dr] = round(weighted_score.get(dr, 0) + f1_score,2)
                highest_weighted_dr = max(weighted_score, key=weighted_score.get)
                
                # Create weighted F1-based dataset
                f1_weighted_dataset[key] = {
                    'text': value['text'],
                    'PT': datasets[0]['data'][key]['PT'],
                    'weighted_score': weighted_score,
                    'DR': highest_weighted_dr, # Based on highest weighted F1 score
                }
        
            if most_common_count >= i:                
                dataset[key] = {
                'text': value['text'],
                'PT': datasets[0]['data'][key]['PT'],
                'all_DRs' : dr_values,
                'DR': most_common_dr
                }

        if not is_weighted_f1_calculated:
            with open(os.path.join(output_path, 'pooled_f1_weighted_dataset.json'), 'w', encoding='utf-8') as f:
                json.dump(f1_weighted_dataset, f, indent=2, ensure_ascii=False )
            is_weighted_f1_calculated = True

            # Add summary for weighted F1 dataset to report
            PT_count = Counter(item["PT"] for item in f1_weighted_dataset.values())
            DR_count = Counter(item["DR"] for item in f1_weighted_dataset.values())

            sorted_PT_count = sorted(PT_count.items(), key=lambda item: item[1], reverse=True)
            sorted_DR_count = sorted(DR_count.items(), key=lambda item: item[1], reverse=True)

            with open (report_path, 'a') as file:
                file.write('f1_weighted_dataset\n')
                file.write(f'Number of instances#: {len(f1_weighted_dataset)}\n[\n')
                for technique, count in sorted_PT_count:
                    file.write(f"    {technique:40}: {count}\n")
                file.write(']\n[')
                for relation, count in sorted_DR_count:
                    file.write(f'    {relation:40}: {count}\n')
                file.write(']\n\n----------------------------------\n\n')




        file_name = f'pooled_agreement_{i}_or_more'
        with open(os.path.join(output_path, f'{file_name}.json'), 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False )


        PT_count = {}
        DR_count = {}
        for key, item in dataset.items():
            dr = item["DR"]
            pt = item["PT"]

            DR_count[dr] = DR_count[dr] + 1 if dr in DR_count else 1
            PT_count[pt] = PT_count[pt] + 1 if pt in PT_count else 1
        

        sorted_PT_count = sorted(PT_count.items(), key = lambda item: item[1], reverse = True)
        sorted_DR_count = sorted(DR_count.items(), key = lambda item: item[1], reverse = True)

        with open (report_path, 'a') as file:
            file.write(f'{file_name}\n')
            file.write(f'Number of instances#: {len(dataset)}\n[\n')
            for technique, count in sorted_PT_count:
                file.write(f"    {technique:40}: {count}\n")
            file.write(']\n[')
            for relation, count in sorted_DR_count:
                file.write(f'    {relation:40}: {count}\n')
            file.write(']\n\n----------------------------------\n\n')







            
            







