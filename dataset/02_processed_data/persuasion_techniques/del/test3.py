import json
import statistics
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
with open('semeval_PT_annotated_dataset.json', 'r') as jsonfile:
    data = json.load(jsonfile)

# Extract number of sentences per text
sentence_counts = {key: len([s for s in entry['text'].split('.') if s.strip()])
                   for key, entry in data.items()}

# Filter dataset for texts containing only up to 2 sentences
filtered_data = {key: value for key, value in data.items() if sentence_counts[key] <= 2}

# Count number of items in the dataset meeting the condition
filtered_count = len(filtered_data)
print(f"Total number of entries with max 2 sentences: {filtered_count}")

# Count persuasion techniques (PT) in filtered data
pt_count = {}
for key, value in filtered_data.items():
    if value['PT'] not in pt_count:
        pt_count[value['PT']] = 1
    else:
        pt_count[value['PT']] += 1

# Save PT count distribution to JSON
with open('filtered_pt_count.json', 'w') as jsonfile:
    json.dump(pt_count, jsonfile, indent=2)

# Display PT distribution
print("Persuasion technique distribution for texts with max 2 sentences:", pt_count)

# Sort persuasion techniques by frequency in descending order
sorted_pt = sorted(pt_count.items(), key=lambda x: x[1], reverse=True)
pt_labels, pt_values = zip(*sorted_pt)

# Create the PT distribution plot with labels on the y-axis, ordered from biggest on top
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=pt_values, y=pt_labels, color=(151/255, 204/255, 232/255))  # Apply extracted color

# Add count labels on each bar
for i, v in enumerate(pt_values):
    ax.text(v + 0.5, i, str(v), color='black', va='center')

plt.title('Distribution of Persuasion Techniques (Max 2 Sentences)')
plt.xlabel('Frequency')
plt.ylabel('Persuasion Technique')
plt.show()
