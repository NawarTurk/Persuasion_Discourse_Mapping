import os
import json
from collections import Counter

def pool_data_and_log_results():
    direct_path = os.path.join('../', 'results', "stage2_DR_parsing_PT_annotated_semeval_datasets", "02_hallucination_removed")
    report_path = os.path.join('../', 'results', "stage2_DR_parsing_PT_annotated_semeval_datasets", "data_pooling_summary.txt")
    output_path = os.path.join('../', 'results', "stage2_DR_parsing_PT_annotated_semeval_datasets", "03_pooled_datasets")

    json_files =[file for file in os.listdir(direct_path) if file.endswith('.json')]
    datasets = []
    files_numb = len(json_files)
    with open (report_path, 'w') as file:
        pass

    for json_file in json_files:
        file_path = os.path.join(direct_path, json_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            datasets.append(json.load(f))

    k = 0
    for i in range(2, files_numb+1):
        dataset = {}
        k = k + 1
        for key, value in datasets[0].items():
            dr_values = [dataset[key]['DR'] for dataset in datasets]
            dr_counter = Counter(dr_values)
            most_common_dr, most_common_count = dr_counter.most_common(1)[0]
        
            if most_common_count >= i:
                if i == files_numb:
                    file_name = f'pooled_agreement_on_all'
                else:
                    file_name = f'pooled_agreement_{i}_or_more'
                
                dataset[key] = {
                'text': value['text'],
                'PT': datasets[0][key]['PT'],
                'all_DRs' : dr_values,
                'DR': most_common_dr
                }

        with open(os.path.join(output_path, f'{file_name}.json'), 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False )

        PT_count = {}
        for key, value in dataset.items():
            if value['PT'] in PT_count:
                PT_count[value['PT']] += 1
            else:            
                PT_count[value['PT']] = 1

        sorted_PT_count = sorted(PT_count.items(), key= lambda item: item[1], reverse=True)

        with open (report_path, 'a') as file:
            file.write(f'{file_name}\n')
            file.write(f'Number of instances#: {len(dataset)}\n[\n')
            for technique, count in sorted_PT_count:
                file.write(f"    {technique:40}: {count}\n")
            file.write(']\n\n----------------------------------\n\n')







            
            







