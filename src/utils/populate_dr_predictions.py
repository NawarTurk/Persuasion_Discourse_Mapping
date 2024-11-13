import json
import os
import time
from prompts.prompt_templates import get_prompt
from utils.llm_prompt_handlers.gpt_prompt_handler import gpt_prompt_handler
from utils.llm_prompt_handlers.gemini_prompt_handler import gemini_prompt_handler
from utils.llm_prompt_handlers.claude_prompt_handler import claude_prompt_handler

import config

dataset_path = os.path.join("..","dataset")
input_file = os.path.join(dataset_path, "02_processed_data", "dr_actual_labels_sample1.json")

prompt_key = config.PROMPT_KEY
parser_id = config.PARSER_ID
delay = config.PROCESSING_DELAY_SECONDS

if parser_id == 1:
    parser = gpt_prompt_handler
    model_name = config.OPENAI_MODEL_NAME
elif parser_id == 2:
    parser = gemini_prompt_handler
    model_name = config.GEMINI_MODEL_NAME
elif parser_id == 3:
    parser = claude_prompt_handler
    model_name = config.CLAUDE_MODEL_NAME
else:
    print("Wrong parser id in config... ")


def populate_dr_predictions():
    print(f"\n\nStarting DR predictions for samples with prompt '{prompt_key} and parser {parser.__name__}'...")

    output_file = os.path.join(dataset_path, "03_results", "dr_sample_prediction", f"dr_predictions_{prompt_key}_sample1_{parser.__name__}.json")

    with open(input_file, 'r', encoding='utf-8') as jsonfile:
        dr_data_samples = json.load(jsonfile)
    
    prompt_template = get_prompt(prompt_key)

    print('\nParser: ', parser.__name__, 'Model Name: ', model_name)

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

    print(f"DR predictions complete. Results saved to: {output_file}")  # End print
    