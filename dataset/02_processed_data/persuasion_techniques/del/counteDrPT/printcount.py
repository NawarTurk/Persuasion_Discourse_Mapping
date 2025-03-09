import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Load the JSON data
with open('drcount.json', 'r') as f:
    dr_counts = json.load(f)

# Sorting DR counts by values in descending order
sorted_dr_counts = dict(sorted(dr_counts.items(), key=lambda item: item[1], reverse=True))

# Extract data
dr_labels, dr_values = zip(*sorted_dr_counts.items())

# Creating the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plotting discourse relations (DR) counts
bars = ax.barh(dr_labels, dr_values, color='skyblue', edgecolor='black')

# Adding value labels at the end of each bar
for bar, value in zip(bars, dr_values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, str(value),
            va='center', ha='left', fontsize=10)

# Formatting the plot
ax.set_xlabel('Count')
# ax.set_title('Discourse Relations Count')
ax.set_xlim(0,20)
ax.invert_yaxis()  # Invert to display the largest count at the top
ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Prevent decimals on the x-axis

plt.tight_layout()
plt.savefig('Discourse_Relations_Count_with_Values.png')
plt.show()



# Creating subplots
fig, ax = plt.subplots(1, 1, figsize=(12, 12), sharex=False)

# Plotting discourse relations (DR) counts
ax[0].barh(dr_labels, dr_values, color='skyblue', edgecolor='black')
ax[0].set_title('Discourse Relations (DR Dataset) Counts ')
# ax[0].set_xlabel('Count')
ax[0].invert_yaxis()  # Invert to display the largest count at the top
ax[0].xaxis.set_major_locator(MaxNLocator(integer=True))  # Prevent decimals on the x-axis

# Plotting persuasion techniques (PT) counts
ax[1].barh(pt_labels, pt_values, color='salmon', edgecolor='black')
ax[1].set_title('Persuasion Techniques (PT Dataset) Counts')
ax[1].set_xlabel('Count')
ax[1].invert_yaxis()  # Invert to display the largest count at the top
ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))  # Prevent decimals on the x-axis

fig.subplots_adjust(hspace=0.8)
plt.tight_layout()
plt.savefig('dr_pt_counts_plot.png')
plt.show()
