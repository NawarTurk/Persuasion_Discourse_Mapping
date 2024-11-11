import json
import os
import time
from prompts.prompt_templates import get_prompt

dataset_path = os.path.join("..","dataset")
input_file = os.path.join(dataset_path, "02_processed_data", "dr_actual_labels_sample1.json")

def populate_dr_predictions_for_dr_samples(prompt_key, parser,delay =3):
    print(f"\n\nStarting DR predictions for samples with prompt '{prompt_key} and parser {parser.__name__}'...")  # Start print

    output_file = os.path.join(dataset_path, "03_results", "dr_sample_prediction", f"dr_predictions_{prompt_key}_sample1_{parser.__name__}.json")

    with open(input_file, 'r', encoding='utf-8') as jsonfile:
        dr_data_samples = json.load(jsonfile)
    
    prompt_template = get_prompt(prompt_key)

    for sample_id, sample in dr_data_samples.items():
        paragrapgh = sample['text']
        print(sample_id)
        dr_prediction = parser(paragrapgh, prompt_template)
        print('the prediction is ...')
        print(dr_prediction)
        sample['predicted_DR_level2'] = dr_prediction

        time.sleep(delay)

    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(dr_data_samples, jsonfile, indent=2, ensure_ascii=False)

    print(f"DR predictions complete. Results saved to: {output_file}")  # End print
