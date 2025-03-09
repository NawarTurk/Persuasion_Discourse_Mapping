import os
import json
import pandas as pd

json_files = sorted(
    [file for file in os.listdir('./') if file.endswith('.json')]
)

DR_lists = {}

for file in json_files:
    parser_key = file[:-8]
    if parser_key not in DR_lists:
        DR_lists[parser_key] = {
            1: {},
            2: {}
        }
        for id in range(1, 127):
            id_str = str(id)
            DR_lists[parser_key][1][id_str] = None
            DR_lists[parser_key][2][id_str] = None
    trial_num = 1 if '_t1' in file else 2

    with open(file) as f:
        data = json.load(f)
        for key,value in data.items():
            DR_lists[parser_key][trial_num][key] = value['predicted_DR_level2']


discrepancy_list = []
for parser_key, value in DR_lists.items():
    trial_1_dict = value[1]
    trial_2_dict = value[2]

    # Calculate percentage agreement
    match_count = sum(
        1 for k in trial_1_dict.keys()
        if trial_1_dict[k] == trial_2_dict[k] and trial_1_dict[k] is not None and trial_2_dict[k] is not None
    )
    agreement_percentage = round((match_count * 100 / 126), 0)
    discrepancy_list.append([parser_key, agreement_percentage])

# Convert to DataFrame
discrepancy_df = pd.DataFrame(discrepancy_list, columns=['Parser', 'Agreement (%)'])
discrepancy_df['prompt_id', 'model']
discrepancy_df.to_excel('parser_discrepancy.xlsx', index=False)

