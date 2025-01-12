

import pandas as pd

# Sample dataframe mimicking the uploaded image
data = {
    'prompt_id': ['promptN01', 'promptN01', 'promptN01', 'promptN01', 'promptN01', 
                  'promptN02', 'promptN02', 'promptN02', 'promptN02', 'promptN02', 
                  'promptN03', 'promptN03', 'promptN03', 'promptN03', 'promptN03',
                  'promptN04', 'promptN04', 'promptN04', 'promptN04', 'promptN04'],
    'model': ['gpt-4o', 'gemini-1.5-flat', 'claude-3-5-son', 'gemini-2.0-flat', 'gpt-4o',
              'gpt-4o', 'gemini-1.5-flat', 'claude-3-5-son', 'gemini-2.0-flat', 'gpt-4o',
              'gpt-4o', 'gemini-1.5-flat', 'gemini-2.0-flat', 'claude-3-5-son', 'gpt-4o',
              'gpt-4o', 'gemini-1.5-flat', 'gemini-2.0-flat', 'claude-3-5-son', 'gpt-4o'],
    'average_f1_n': [0.26, 0.30, 0.40, 0.27, 0.27, 
                     0.28, 0.31, 0.34, 0.38, 0.30, 
                     0.30, 0.35, 0.36, 0.38, 0.29, 
                     0.29, 0.30, 0.34, 0.33, 0.31],
    'average_acc': [0.34, 0.36, 0.46, 0.36, 0.35, 
                    0.37, 0.37, 0.42, 0.45, 0.39, 
                    0.39, 0.44, 0.46, 0.45, 0.35, 
                    0.40, 0.35, 0.43, 0.44, 0.43]
}

df = pd.DataFrame(data)

# Grouping by 'prompt_id' and calculating the average of 'average_f1_n' and 'average_acc'
summary = df.groupby('prompt_id').agg({
    'average_f1_n': 'mean',
    'average_acc': 'mean'
}).reset_index()

import ace_tools as tools; tools.display_dataframe_to_user(name="Summary of Prompt ID Averages", dataframe=summary)
