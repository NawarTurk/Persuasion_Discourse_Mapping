import json
import os
import time
from utils.llm_prompt_handlers.gpt_prompt_handler import gpt_prompt_handler
from utils.llm_prompt_handlers.gemini_prompt_handler import gemini_prompt_handler
from utils.llm_prompt_handlers.claude_prompt_handler import claude_prompt_handler
from utils.llm_prompt_handlers.multi_level_gpt_prompt_handler_v1 import multi_level_gpt_prompt_handler_v1
from utils.llm_prompt_handlers.multi_level_gpt_prompt_handler_v2 import multi_level_gpt_prompt_handler_v2
from utils.llm_prompt_handlers.multi_level_gemini_prompt_handler_v1 import multi_level_gemini_prompt_handler_v1
from utils.llm_prompt_handlers.multi_level_gemini_prompt_handler_v2 import multi_level_gemini_prompt_handler_v2
from utils.llm_prompt_handlers.multi_level_claude_prompt_handler_v1 import multi_level_claude_prompt_handler_v1
from utils.llm_prompt_handlers.multi_level_claude_prompt_handler_v2 import multi_level_claude_prompt_handler_v2



from prompts.prompt_template_getter import get_prompt_template
from datetime import datetime

import config


dataset_path = os.path.join("..","dataset")
results = os.path.join("..","results")
input_file = os.path.join(dataset_path, "02_processed_data", "discourse_relations", "DR_labeled_sample1_126instances.json") # change me


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
elif parser_id == 9:
    parser = multi_level_gpt_prompt_handler_v1
    model_name = config.OPENAI_MODEL_NAME + '_multi_level_V1'
elif parser_id == 10:
    parser = multi_level_gpt_prompt_handler_v2
    model_name = config.OPENAI_MODEL_NAME + '_multi_level_V1'
elif parser_id == 11:
    parser = multi_level_gemini_prompt_handler_v1
    model_name = config.GEMINI_MODEL_NAME + '_multi_level_V1'
elif parser_id == 12:
    parser = multi_level_gemini_prompt_handler_v2 
    model_name = config.GEMINI_MODEL_NAME + '_multi_level_V2'
elif parser_id == 13:
    parser = multi_level_claude_prompt_handler_v1
    model_name = config.CLAUDE_MODEL_NAME + '_multi_level_V1'
elif parser_id == 14:
    parser = multi_level_claude_prompt_handler_v2
    model_name = config.CLAUDE_MODEL_NAME + '_multi_level_V2'

else:
    print("Wrong parser id in config... ")

prompt_template = get_prompt_template(prompt_key)
date = datetime.now().strftime('%b-%d-%a-%H-%M')
output_file = os.path.join(results, "stage1_eval_initial_DR_prompts_126instances", "json_DR_level2_predictions", f"{prompt_key}_{model_name}_{date}.json")



def parser_DR_with_LLM():
    print(f"\n\n###### Starting DR predictions for the PDTB sample data ######\n")
    print(f'using {parser.__name__} parser. \nModel Name: , {model_name}')

    with open(input_file, 'r', encoding='utf-8') as jsonfile:
        dr_data_samples = json.load(jsonfile)
    
    print("\n______The Prompt Template_____")
    print(prompt_template)
    print("______________________________\n")

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

    print(f"DR predictions complete. Results saved to: {output_file}") 
    