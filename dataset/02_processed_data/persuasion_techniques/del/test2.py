import json
import statistics
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
with open('semeval_PT_annotated_dataset.json', 'r') as jsonfile:
    data = json.load(jsonfile)

# Extract text lengths into a list for statistical analysis
text_lengths = [len(entry['text']) for entry in data.values()]
average_length = statistics.mean(text_lengths)
standard_deviation = statistics.stdev(text_lengths)

print(f"Average text length calculated using statistics module: {average_length:.2f}")
print(f"Standard deviation of text lengths: {standard_deviation:.2f}")

min_length = min(text_lengths)
print(f"Minimum text length: {min_length}")

max_length = max(text_lengths)
print(f"Maximum text length: {max_length}")

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Create the text length distribution plot
plt.figure(figsize=(10, 6))  # Set the figure size
sns.histplot(text_lengths, binwidth=10, kde=True, color='blue')  # Histogram with KDE and specified bin width

# Adding titles and labels
plt.title('Distribution of Text Lengths')
plt.xlabel('Text Length')
plt.ylabel('Frequency')
plt.xticks(range(min_length, max_length + 10, 10))  # Ensuring all x-axis labels are shown

# Display the plot
plt.show()

count = {}
for key, value in data.items():
    if value['PT'] not in count:
        count[value['PT']] = 1
    else:
        count[value['PT']] += 1

with open('count.json', 'w') as jsonfile:
    json.dump(count, jsonfile, indent=2)

print(f"Total entries in dataset: {len(data)}")

# Extract number of sentences per text
sentence_counts = [len([s for s in entry['text'].split('.') if s.strip()])
                   for entry in data.values()]

average_sentence_count = statistics.mean(sentence_counts)
min_sentence_count = min(sentence_counts)
max_sentence_count = max(sentence_counts)

print(f"Average number of sentences per text: {average_sentence_count:.2f}")
print(f"Minimum number of sentences per text: {min_sentence_count}")
print(f"Maximum number of sentences per text: {max_sentence_count}")

# Create the sentence count distribution plot
plt.figure(figsize=(10, 6))
sns.histplot(sentence_counts, binwidth=1, kde=True, color='red')
plt.title('Distribution of Sentence Counts per Text')
plt.xlabel('Number of Sentences')
plt.ylabel('Frequency')
plt.xticks(range(min_sentence_count, max_sentence_count + 1, 1))  # Ensuring all x-axis labels are shown

# Add max marker for 10 sentences
plt.axvline(x=10, color='black', linestyle='--', label='Max for 10 Sentences')
plt.legend()

plt.show()
