import os
import json
import pandas as pd
from utils.helpers.pt_dr_getters import get_level2_DR_id_by_name
import warnings
from sklearn.metrics import f1_score, classification_report, accuracy_score
from sklearn.exceptions import UndefinedMetricWarning
import matplotlib.pyplot as plt


warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

dataset_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "json_DR_level2_predictions")
output_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "metrics_level2")
summary_report_xlsx_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level2_metrics_summary.xlsx")
summary_avg_report_xlsx_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level2_avg_metrics_summary.xlsx")
summary_avg_prompt_aggregated_report_xlsx_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level2_metrics_summary_aggregated_by_prompt.xlsx")
summary_avg_model_aggregated_report_xlsx_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level2_metrics_summary_aggregated_by_model.xlsx")


average_f1_scores_level2_per_parser = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "average_f1_scores_level2_per_parser.json")


plot_output_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level2_model_f1_macro_by_prompt.png")
plot_avg_output_path = os.path.join("..", "results", "stage1_eval_initial_DR_prompts_126instances", "summary_report", "level2_model_avg_f1_macro_by_prompt.png")

# Add a numeric ID column to the DataFrame
def assign_numeric_id(prompt_id):
    if 'N' in prompt_id:
        # Extract the number after 'N' and return as integer
        return int(prompt_id.replace('promptN', ''))
    
def evaluate_DR_parser_with_f1(): 
    summary_report = {}
    avg_f1_values = {}
    global_class_f1_scores = {}


    for filename in os.listdir(dataset_path):
        if filename.endswith('.json'):
            input_file= os.path.join(dataset_path, filename)

            with open(input_file, 'r', encoding='utf-8') as jsonfile:

                dataset = json.load(jsonfile)
                dr_true = [get_level2_DR_id_by_name(sample['actual_DR_level2'].lower()) for _, sample in dataset.items()]
                dr_pred = [get_level2_DR_id_by_name(sample['predicted_DR_level2']) for _, sample in dataset.items()]

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

                output_filename = f"level2_metrics_{filename.replace('.json', '.txt')}"
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
                    'level': 'level2',
                    'f1_macro': round(f1_macro, 3),
                    'f1_micro': round(f1_micro, 3),
                    'f1_weighted': round(f1_weighted, 3),
                    'accuracy': round(accuracy, 3),
                    'faulty_predictions_numb': numb_faulty_results,
                    'adjusted_accuracy': adjusted_accuracy
                }

                key = f'{model_name}_{prompt_id}'
                if key not in avg_f1_values:
                    avg_f1_values[key] = {
                        'f1_macro_values': [],
                        'accuracy_values': [],
                        'faulty_predictions_numb': []
                    }
                avg_f1_values[key]['f1_macro_values'].append(round(f1_macro,3))
                avg_f1_values[key]['accuracy_values'].append(round(adjusted_accuracy,3))
                avg_f1_values[key]['prompt_id'] = prompt_id 
                avg_f1_values[key]['model'] = model_name 
                avg_f1_values[key]['faulty_predictions_numb'].append(numb_faulty_results)


                    ###
                report_dict = classification_report(dr_true, dr_pred, digits=3, output_dict=True)
                f1_by_class = {class_label: metrics['f1-score'] 
                    for class_label, metrics in report_dict.items() 
                    if class_label.isdigit()}
                
                if key not in global_class_f1_scores:
                    global_class_f1_scores[key] = {class_label: {'f1_values': []} for class_label in f1_by_class}

                for class_label, f1_score_value in f1_by_class.items():
                    try:
                        global_class_f1_scores[key][class_label]['f1_values'].append(f1_score_value)
                    except:
                        continue
                  
    for parser, class_labels in global_class_f1_scores.items():
        for class_label, value in class_labels.items():
             value['average_f1_score'] = sum(value['f1_values']) / len(value['f1_values'])

    
    for key, value in avg_f1_values.items():
        value['average_f1_macro'] = sum(value['f1_macro_values'])/len(value['f1_macro_values'])
        value['average_accuracy'] = sum(value['accuracy_values'])/len(value['accuracy_values'])
        value['faulty_predictions_numb'] = sum(value['faulty_predictions_numb'])/len(value['faulty_predictions_numb'])


    df = pd.DataFrame.from_dict(summary_report, orient = 'index')
    df_avg = pd.DataFrame.from_dict(avg_f1_values, orient = 'index')
    # Apply the function to create the numeric_id column
    df['numeric_id'] = df['prompt_id'].apply(assign_numeric_id)
    df_avg['numeric_id'] = df_avg['prompt_id'].apply(assign_numeric_id)
   
    # Sort the DataFrame by the numeric_id
    df = df.sort_values('numeric_id')
    df_avg = df_avg.sort_values('numeric_id')
    df.to_excel(summary_report_xlsx_path, index=False)
    df_avg.to_excel(summary_avg_report_xlsx_path, index =False)

    prompt_aggregated = df_avg.groupby('prompt_id').agg({
        'average_f1_macro': 'mean',
        'average_accuracy': 'mean',
        'faulty_predictions_numb': 'mean'
    }).reset_index()
    prompt_aggregated.to_excel(summary_avg_prompt_aggregated_report_xlsx_path, index=False)

    model_aggregated = df_avg.groupby('model').agg({
        'average_f1_macro': ['mean', 'max', 'min'],
        'average_accuracy': 'mean',
        'faulty_predictions_numb': 'mean',
        'faulty_predictions_numb': 'mean'
    }).reset_index()
    model_aggregated.columns = ['_'.join(col).strip('_') for col in model_aggregated.columns.values]
    model_aggregated.to_excel(summary_avg_model_aggregated_report_xlsx_path, index=False)



    with open(average_f1_scores_level2_per_parser, 'w') as f:
        json.dump(global_class_f1_scores, f, indent=4)

    

    


    plt.figure(figsize=(12, 8))
    # Plot each model as a separate line
    for model in df['model'].unique():
        subset = df[df['model'] == model]
        plt.plot(subset['prompt_id'], subset['f1_macro'], marker='o', label=model)
    # Customizing the plot
    plt.xlabel('Prompt ID')
    plt.ylabel('Macro F1 Score')
    plt.legend(title='Model', loc='upper right')
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability
    plt.tight_layout()  # Adjust layout to prevent label clipping
    plt.ylim(0.1, 0.5)
    plt.savefig(plot_output_path, format='png', dpi=300)
    # plt.show()

    plt.figure(figsize=(12,8))
    for model in df_avg['model'].unique():
        subset = df_avg[df_avg['model'] == model]
        plt.plot(subset['prompt_id'], subset['average_f1_macro'], marker='o', label=model)
    plt.xlabel('Prompt ID')
    plt.ylabel('Average Macro F1 Score')
    plt.legend(title='Model', loc='upper right')
    plt.grid(True)
    plt.ylim(0.1,0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{plot_avg_output_path}', format ='png', dpi=300)
    # plt.show()


    
