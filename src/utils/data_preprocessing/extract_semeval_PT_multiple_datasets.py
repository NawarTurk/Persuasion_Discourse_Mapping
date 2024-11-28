import os
import json

def extract_semeval_PT_multiple_datasets():

    print("\nDividing the large SemEval dataset into smaller, datasets with specific counts of each persuasion technique...\n\n\n")

    dataset_path = os.path.join( "..", "dataset")
    input_json_path=os.path.join(dataset_path, "02_processed_data", "persuasion_techniques", "semeval_PT_annotated_dataset.json")
    ouput_path = os.path.join(dataset_path, "02_processed_data", "persuasion_techniques", 'divided_semval_PT_datasets')
    with open(input_json_path, 'r') as jsonfile:
        global_PT_data = json.load(jsonfile)

    desired_count_per_dataset = {
        'Doubt': 90,
        'Appeal_to_Authority': 90,
        'Repetition': 90,
        'Appeal_to_Fear-Prejudice': 90,
        'Slogans': 90,
        'False_Dilemma-No_Choice': 90,
        'Loaded_Language': 90,
        'Flag_Waving': 90,
        'Name_Calling-Labeling': 90,
        'Causal_Oversimplification': 90,
        'Appeal_to_Hypocrisy': 40,  # max available
        'Obfuscation-Vagueness-Confusion': 18,  # max available
        'Exaggeration-Minimisation': 90,
        'Red_Herring': 44,  # max available
        'Guilt_by_Association': 59,  # max available
        'Conversation_Killer': 90,
        'Appeal_to_Popularity': 15,  # max available
        'Straw_Man': 15,  # max available
        'Whataboutism': 16   # max available
    }

    num_of_datasets = 10

    PT_datasets = [{} for dataset in range(num_of_datasets)]

    dataset_PT_counts = [{pt: 0 for pt in desired_count_per_dataset} for dataset in range(num_of_datasets)] 

    used_entries = set()


    for dataset_index in range(num_of_datasets):
        for key, entry in global_PT_data.items():
            if key not in used_entries:
                PT_type = entry['PT']
                if dataset_PT_counts[dataset_index][PT_type] < desired_count_per_dataset[PT_type]:
                    PT_datasets[dataset_index][key] = entry
                    dataset_PT_counts[dataset_index][PT_type] += 1
                    used_entries.add(key)

    for dataset_index, dataset in enumerate(PT_datasets):
        partial_PT_dataset_path = os.path.join(ouput_path, f'semeval_PT_dataset_{dataset_index+1}.json')
        with open(partial_PT_dataset_path, 'w') as file:
            json.dump(dataset,file, indent=2)
            print(f'semeval_PT_dataset_{dataset_index}.json is saved in 02_processed_data/persuasion_techniques/divided_semeval_PT_datasets')

    # for Validation
    # PT ={}
    # for key, entry in PT_datasets[1].items():
    #     pt_entry = {
    #         entry['PT']
    #     }

    #     if entry['PT'] not in PT:
    #         PT[entry['PT']] = []

    #     PT[entry['PT']].append(pt_entry)

    # for key, value in  PT.items():
    #     print(f'{key}    ......    .......    ......   {len(value)}')  
