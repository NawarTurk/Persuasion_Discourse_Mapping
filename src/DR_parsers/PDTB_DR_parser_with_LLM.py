import json
import config
import os
import time
from utils.helpers.get_parser_and_model_name import get_parser_and_model_name
from prompts.prompt_template_getter import get_prompt_template
from datetime import datetime

prompt_key = config.PROMPT_KEY
parser_id = config.PARSER_ID
delay = config.PROCESSING_DELAY_SECONDS
parser, model_name = get_parser_and_model_name(parser_id)
prompt_template = get_prompt_template(prompt_key)

date = datetime.now().strftime('%b-%d-%a-%H-%M')
dataset_path = os.path.join("..","dataset")
input_file = os.path.join(dataset_path, "02_processed_data", "discourse_relations", "DR_labeled_sample1_126instances.json") 
# output_file = os.path.join("..","results", "stage1_eval_initial_DR_prompts_126instances", "json_DR_level2_predictions", f"{prompt_key}_{model_name}_t2.json")
output_file = os.path.join("..","results", "stage1_eval_initial_DR_prompts_126instances", "json_DR_level2_predictions", f"{prompt_key}_finetuning_t2.json")


def parser_DR_with_LLM():
    print('''
        \n\n###### Starting DR predictions for PDTB sample data dataset ######
        prompt ID: {0}
        LLM Model: {1}
        Parser: {2}
        '''.format(prompt_key, model_name, parser.__name__))
    time.sleep(3)

    with open(input_file, 'r', encoding='utf-8') as jsonfile:
        dr_data_samples = json.load(jsonfile)
    
    print("\n\n______The Prompt Template_____")
    print(prompt_template)
    print("______________________________\n\n")

    for sample_id, sample in dr_data_samples.items():
        paragraph = sample['text']

        print('\nSample #: ', sample_id)
        actual_DR_level2 = sample['actual_DR_level2']
        print('The actual DR label is: '.ljust(30), actual_DR_level2.rjust(20))

        dr_prediction = parser(paragraph, prompt_template).lower()
        print('The prediction is: '.ljust(30), dr_prediction.rjust(20), '\n')
        sample['predicted_DR_level2'] = dr_prediction

        time.sleep(delay)

    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(dr_data_samples, jsonfile, indent=2, ensure_ascii=False)

    print(f"DR predictions complete.") 
    