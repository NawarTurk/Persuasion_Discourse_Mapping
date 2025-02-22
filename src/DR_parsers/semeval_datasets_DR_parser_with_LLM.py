import logging
import config
import os
import json
import time
from prompts.prompt_template_getter import get_prompt_template
from utils.helpers.get_parser_and_model_name import get_parser_and_model_name

prompt_key = config.PROMPT_KEY
parser_id = config.PARSER_ID
pt_dataset_num = config.PT_DATASET
batch_size = config.BATCH_SIZE
api_call_delay = config.API_CALL_DELAY_SEC
run_delay = config.RUN_DELAY_SEC

parser, model_name = get_parser_and_model_name(parser_id)
prompt_template = get_prompt_template(prompt_key)
    
dataset_path = os.path.join("..","dataset")
results_path = os.path.join('..', 'results', "stage2_DR_parsing_of_PT_annotated_semeval_datasets")
input_path = os.path.join(results_path, '01_with_hallucination', f'{pt_dataset_num}_{model_name}_{prompt_key}.json')

if not os.path.isfile(input_path):
    print(' im hrer')
    input_path = os.path.join(dataset_path, '02_processed_data', "persuasion_techniques", f'{pt_dataset_num}.json')

output_file = os.path.join(results_path, '01_with_hallucination', f'{pt_dataset_num}_{model_name}_{prompt_key}.json')

DR_level2 = {
        "synchronous", "asynchronous", "cause", "cause+belief", "cause+speechact", "condition", "condition+speechact", "negative-condition", 
        "negative-condition+speechact", "purpose", "concession", "concession+speechact", "contrast", "similarity", "conjunction", "disjunction", 
        "equivalence", "exception", "instantiation", "level-of-detail", "manner", "substitution"}

def update_progress(progress, total):   
    percent = 100 * (progress / float(total))
    bar_length = 30  # Length of the progress bar
    filled_length = int(round(bar_length * progress / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    print(f"\rProgress: |{bar}| {percent:.2f}%\n", end="\r")

def semeval_datasets_DR_parser():
    """
    Processes the SemEVal datasets to predict and append discourse relations (DR) using specified parser and prompt.
    Utilizes batch processing and API calls to fetch DR predictions and updates the dataset accordingly.
    """

    with open(input_path, 'r', encoding='utf-8') as file:
        pt_dataset= json.load(file)
        
    total_parsed_entries = sum(1 for _, entry in pt_dataset.items() if entry['DR'] != '')

    print('''
          \n\n###### Starting DR predictions for {0} dataset ######
          prompt ID: {1}
          LLM Model: {2}
          Parser: {3}
          Dataset: {4}
          Current DR Parsing %: {5}
          Saves after {6} instances.
          '''.format(pt_dataset_num, prompt_key, model_name, parser.__name__, pt_dataset_num, round(100*total_parsed_entries/len(pt_dataset), 2), batch_size))
    
    while total_parsed_entries < len(pt_dataset):
        try:
            current_batch_count = 0
            for i, (_, entry) in enumerate(pt_dataset.items()):
                if current_batch_count >= batch_size:
                    break
                if entry['predicted_DR'] == '':
                    paragraph = entry['text']
                    dr_prediction = parser(paragraph, prompt_template).lower()
                    entry['predicted_DR'] = dr_prediction   
                    entry['parser'] = f'{model_name}_{prompt_key}'
                    if dr_prediction in DR_level2:
                        entry['DR'] = dr_prediction
                    else:
                        entry['DR'] = 'NA'

                    current_batch_count += 1
                    total_parsed_entries += 1
                    print(f'\nText #{i} is:\n "{paragraph}')
                    print('The prediction is: '.ljust(30), dr_prediction.rjust(20))
                    print(f'wait time for {api_call_delay} seconds .....')
                    update_progress(total_parsed_entries, len(pt_dataset))
                    time.sleep(api_call_delay)
            with open(output_file, 'w', encoding='utf-8') as jsonfile:
                json.dump(pt_dataset, jsonfile, indent=2, ensure_ascii=False)
            print(f'\n{current_batch_count} instances were saved ...')

        except Exception as e:
            logging.error(f"Error: {e}")
            continue
        
        print(f'The wait time before the second batch is {run_delay}\n')
        time.sleep(run_delay)

            
    print(f"DR predictions for {pt_dataset_num} is complete. Results saved to: {output_file}") 
    print(f'{pt_dataset_num} is {round(100*total_parsed_entries/len(pt_dataset), 3)}% parsed with DR')




