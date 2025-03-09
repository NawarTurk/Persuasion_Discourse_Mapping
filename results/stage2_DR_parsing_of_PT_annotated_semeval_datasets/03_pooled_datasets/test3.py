import json
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

# Define dataset filename
DATASET_FILENAME = 'pooled_agreement_9_or_more.json'
MAX_SENTENCES = 2


# Load the dataset
with open(DATASET_FILENAME, 'r') as jsonfile:
    data_original = json.load(jsonfile)





def count_sentences(text):
    """Helper function to count the number of sentences in a given text."""
    return len([s for s in text.split('.') if s.strip()])


#     return len([s for s in text.split('.') if s.strip()])

def analyze_sentence_distribution(data, title, color, total_entries):
    """Helper function to calculate and plot the actual count distribution of sentences with total size info."""
    sentence_counts = [count_sentences(entry['text']) for entry in data.values()]
    sentence_freq = Counter(sentence_counts)
    
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=list(sentence_freq.keys()), y=list(sentence_freq.values()), color=color)
    plt.xticks(range(min(sentence_freq.keys()), min(max(sentence_freq.keys()), 10) + 1))  # Force x-axis range between 1 and 10
    plt.title(title)
    plt.xlabel('Number of Sentences')
    plt.ylabel('Frequency')
    
    # Add count labels on each bar
    for i, (x, v) in enumerate(sentence_freq.items()):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
    
    # Add total entries info as a box
    text_box = f"Total Entries: {total_entries}"
    plt.text(0.95, 0.95, text_box, transform=plt.gca().transAxes,
             fontsize=12, verticalalignment='top', horizontalalignment='right',
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
    
    plt.show()
    return sentence_counts

def count_persuasion_techniques(filtered_data):
    """Helper function to count persuasion techniques and plot their distribution."""
    pt_count = Counter(value['PT'] for value in filtered_data.values())
    total_pt = sum(pt_count.values())  # Total number of PT occurrences
    
    # Find PTs that appear more than 25 times
    high_freq_pts = [pt for pt, count in pt_count.items() if count > 25]
    high_freq_count = len(high_freq_pts)
    
    # Save PT count distribution to JSON
    with open('filtered_pt_count.json', 'w') as jsonfile:
        json.dump(pt_count, jsonfile, indent=2)
    
    # Display PT distribution
    print("Persuasion technique distribution for texts with max 2 sentences:", pt_count)
    
    # Sort persuasion techniques by frequency in descending order
    sorted_pt = sorted(pt_count.items(), key=lambda x: x[1], reverse=True)
    pt_labels, pt_values = zip(*sorted_pt) if sorted_pt else ([], [])
    
    # Create the PT distribution plot with labels on the y-axis, ordered from biggest on top
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=pt_values, y=pt_labels, color=(151/255, 204/255, 232/255))  # Apply extracted color
    
    # Add count labels on each bar
    for i, v in enumerate(pt_values):
        ax.text(v + 0.5, i, str(v), color='black', va='center')
    
    # Add total PT count as a box in the graph (Top Right)
    text_box = f"Total PT Count: {total_pt}"
    plt.text(0.95, 0.95, text_box, transform=plt.gca().transAxes,
             fontsize=12, verticalalignment='top', horizontalalignment='right',
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
    
    # Add unique high-frequency PT count in the lower right corner
    if high_freq_count > 0:
        high_freq_text = f"PTs > 25: {high_freq_count}"
        plt.text(0.95, 0.05, high_freq_text, transform=plt.gca().transAxes,
                 fontsize=10, verticalalignment='bottom', horizontalalignment='right',
                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
    
    plt.title('Distribution of Persuasion Techniques')
    plt.xlabel('Frequency')
    plt.ylabel('Persuasion Technique')
    plt.show()

# Analyze sentence distribution in original dataset
analyze_sentence_distribution(data_original, 'Distribution of Sentence Counts in Original Data', 'blue', len(data_original))

# Filter dataset for texts containing only up to 2 sentences
filtered_data = {key: value for key, value in data_original.items() if count_sentences(value['text']) <= MAX_SENTENCES}

# Save filtered dataset with modified filename
filtered_filename = f"{DATASET_FILENAME.replace('.json', '')}_filtered_{MAX_SENTENCES}.json"
with open(filtered_filename, 'w') as jsonfile:
    json.dump(filtered_data, jsonfile, indent=2)

# Analyze sentence distribution in filtered dataset
analyze_sentence_distribution(filtered_data, f'Distribution of Sentence Counts in Filtered Data (Max {MAX_SENTENCES} Sentences)', 'green', len(filtered_data))

# Count and plot persuasion technique distribution in original and filtered data
count_persuasion_techniques(data_original)
count_persuasion_techniques(filtered_data)

print(f"Total number of original entries: {len(data_original)}")
print(f"Total number of entries with max {MAX_SENTENCES} sentences: {len(filtered_data)}")
print(f"Filtered dataset saved as: {filtered_filename}")
