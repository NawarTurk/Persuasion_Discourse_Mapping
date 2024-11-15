
import os
import json
from utils.pt_dr_getters import get_DR_id_by_name
import warnings
from sklearn.metrics import f1_score, classification_report, accuracy_score
from sklearn.exceptions import UndefinedMetricWarning
from utils.get_level1_DR import get_level1_DR



warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

dataset_path = os.path.join("..", "dataset", "03_results", "prompt_model_DR_tests")

def get_level1_id(level1_name):
    # Define a dictionary to map level-1 categories to numbers
    level1_to_number = {
        "temporal": 1,
        "contingency": 2,
        "comparison": 3,
        "expansion": 4
    }
    return level1_to_number.get(level1_name, None)


def evaluate_DR_parser_with_f1_lvl1(): 
    for filename in os.listdir(dataset_path):
        if filename.endswith('.json'):
            input_file= os.path.join(dataset_path, filename)

            with open(input_file, 'r', encoding='utf-8') as jsonfile:

                dataset = json.load(jsonfile)
                dr_true = [get_level1_id(sample['actual_DR_level1'].lower()) for _, sample in dataset.items()]
                dr_pred = [get_level1_id(get_level1_DR(sample['predicted_DR_level2'])) for _, sample in dataset.items()]
         
                f1_macro = f1_score(dr_true, dr_pred, average='macro')
                f1_micro = f1_score(dr_true, dr_pred, average='micro')
                f1_weighted = f1_score(dr_true, dr_pred, average='weighted')
                accuracy = accuracy_score(dr_true, dr_pred)


                report = classification_report(dr_true, dr_pred, digits=3)

                output_content = f"F1 Scores for {filename}:\n\n"
                output_content += f"F1 Macro: {f1_macro:.3f}\n"
                output_content += f"F1 Micro: {f1_micro:.3f}\n"
                output_content += f"F1 Weighted: {f1_weighted:.3f}\n\n"
                output_content += f"Accuracy: {accuracy:.3f}\n\n"
                output_content += "Classification Report:\n"
                output_content += report

                output_filename = f"lvl1_f1_{filename.replace('.json', '.txt')}"
                output_file = os.path.join(dataset_path, output_filename)

                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.write(output_content)

                print('\n-----------------')
                print(f"Saved F1 scores and report for {filename} to {output_filename}")


    



 
