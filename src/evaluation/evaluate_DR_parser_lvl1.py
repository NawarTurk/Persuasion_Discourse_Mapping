import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from utils.helpers.pt_dr_getters import get_DR_id_by_name
import warnings
from sklearn.metrics import f1_score, classification_report, accuracy_score
from sklearn.exceptions import UndefinedMetricWarning
from utils.helpers.get_level1_DR import get_level1_DR

warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

dataset_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "json_DR_level2_predictions")
output_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "metrics_level1")
summary_report_json_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level1_metrics_summary.json")
summary_report_xlsx_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level1_metrics_summary.xlsx")
plot_output_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level1_model_accuracy_by_prompt.png")

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
    summary_report = {}

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

                output_filename = f"level1_metrics_{filename.replace('.json', '.txt')}"
                output_file = os.path.join(output_path, output_filename)

                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.write(output_content)

                print('\n-----------------')
                print(f"Saved F1 scores and report for {filename} to {output_filename}")
                
                filename_segments = filename.split('_')
                prompt_id = filename_segments[0]
                model_name = filename_segments[1]

                # Accounting for hallucinations that were removed manually from some experiments
                numb_faulty_results = 126 - len(dataset)
                num_correct_predictions = accuracy * len(dataset)
                adjusted_accuracy = round(num_correct_predictions/126, 3)

                summary_report[len(summary_report) + 1] = {
                    'prompt_id': prompt_id,
                    'model': model_name,
                    'level': 'level1',
                    'f1_macro': round(f1_macro, 3),
                    'f1_micro': round(f1_micro, 3),
                    'f1_weighted': round(f1_weighted, 3),
                    'accuracy': round(accuracy, 3),
                    'faulty_predictions_numb': numb_faulty_results,
                    'adjusted_accuracy': adjusted_accuracy
                }

    with open(summary_report_json_path, 'w') as jsonfile:
        json.dump(summary_report, jsonfile, indent = 2)


    df = pd.DataFrame.from_dict(summary_report, orient= 'index')
    df.to_excel(summary_report_xlsx_path, index=False)


    # Add a numeric ID column to the DataFrame
    def assign_numeric_id(prompt_id):
        if 'N' in prompt_id:
            # Extract the number after 'N' and return as integer
            return int(prompt_id.replace('promptN', ''))
        elif 'S' in prompt_id:
            return 50 + int(prompt_id.replace('promptS', ''))
        elif 'COT' in prompt_id:
            # Extract the number after 'COT', offset by 50
            return 100 + int(prompt_id.replace('promptCOT', ''))
        else:
            # Default case for unexpected formats
            return 150

    # Apply the function to create the numeric_id column
    df['numeric_id'] = df['prompt_id'].apply(assign_numeric_id)

    # Sort the DataFrame by the numeric_id
    df = df.sort_values('numeric_id')

    # Plotting
    plt.figure(figsize=(12, 8))

     # Plot each model as a separate line
    for model in df['model'].unique():
        subset = df[df['model'] == model]
        plt.plot(subset['prompt_id'], subset['adjusted_accuracy'], marker='o', label=model)

        # Annotate each point with the adjusted accuracy value
        for i, row in subset.iterrows():
            # Conditional positioning for annotations
            if row['adjusted_accuracy'] < 0.4:
                vertical_alignment = 'top'
                vertical_offset = -0.03
            else:
                vertical_alignment = 'bottom'
                vertical_offset = 0.03
            
            plt.text(row['prompt_id'], row['adjusted_accuracy'] + vertical_offset,
                    f"{row['adjusted_accuracy']:.2f}", fontsize=8, ha='center', va=vertical_alignment)

    # Customizing the plot
    plt.xlabel('Prompt ID')
    plt.ylabel('Accuracy')
    plt.legend(title='Model', loc='upper right')
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability
    plt.tight_layout()  # Adjust layout to prevent label clipping
    plt.ylim(0, 1)
    plt.savefig(plot_output_path, format='png', dpi=300)
    plt.show()



    
