import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick  # Import for formatting y-axis labels

# Creating the dataset
# Columns: Prompt ID, Listed Label Levels, Definition Label Level, Examples, Text Segmentations, Macro F1 Score, Faulty Predictions, Hallucinations
data = {
    'Prompt ID': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
    'Macro F1 Score': [0.30, 0.33, 0.35, 0.32, 0.35, 0.29, 0.29, 0.28, 0.27, 0.25, 0.26],
    'Faulty Predictions': [1, 2, 4, 0, 5, 4, 8, 11, 15, 15, 0],
    'Hallucinations': [1, 2, 4, 0, 5, 4, 8, 11, 15, 15, 0],  # Placeholder for hallucinations
    'Segmentation': ['No', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes']  # Segmentation instruction
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Round Macro F1 Score to two decimal places
df['Macro F1 Score'] = df['Macro F1 Score'].round(2)

# Define color mapping based on segmentation instructions
colors = ['blue' if seg == 'No' else 'orange' for seg in df['Segmentation']]

# Define positions for the scatter points
x_positions = np.arange(len(df['Prompt ID']))

# Create the figure
plt.figure(figsize=(12, 12))

# Subplot for Macro F1 Score
plt.subplot(2, 1, 1)
plt.scatter(x_positions, df['Macro F1 Score'], color=colors, s=100, alpha=0.8, marker='o')
plt.title('Macro F1 Score by Prompt ID', fontsize=14)
plt.ylabel('Macro F1 Score', fontsize=12)
plt.ylim(0.22, 0.4)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tick_params(axis='x', which='both', bottom=False, labelbottom=False)  # Remove x-axis labels and ticks
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))  # Format y-axis labels to 2 decimal places


# Annotate API call for prompt 11 in the upper plot
plt.annotate('via two API calls', (x_positions[-1], df['Macro F1 Score'].iloc[-1]),
             textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color='black')

# Legend for color mapping in the upper plot
plt.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='blue', label='No Segmentation Instruction', markersize=10, linestyle=''),
    plt.Line2D([0], [0], marker='o', color='orange', label='With Segmentation Instruction', markersize=10, linestyle='')
], loc='upper right', fontsize=10)

# Subplot for Hallucinations
plt.subplot(2, 1, 2)
plt.scatter(x_positions, df['Hallucinations'], color=colors, s=100, alpha=0.8, marker='o')
plt.title('Hallucinations by Prompt ID', fontsize=14)
plt.ylabel('Hallucinations', fontsize=12)
plt.ylim(-1, 16)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate API call for prompt 11 in the lower plot
plt.annotate('via two API calls', (x_positions[-1], df['Hallucinations'].iloc[-1]),
             textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color='black')


# Customize the x-axis labels only for the bottom subplot
plt.xticks(x_positions, df['Prompt ID'], fontsize=10)

plt.tight_layout()
plt.subplots_adjust(hspace=0.15)  # Adjust the height spacing between the two subplots
plt.savefig('macro_f1_and_hallucinations_subplots_corrected.png')
plt.show()