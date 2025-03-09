import matplotlib.pyplot as plt
import matplotlib.ticker as mticker 
# # # Define the data
# # persuasion_techniques = {
# #     "Loaded_Language": 373,
# #     "Name_Calling-Labeling": 362,
# #     "Repetition": 333,
# #     "Doubt": 309,
# #     "Exaggeration-Minimisation": 287,
# #     "Appeal_to_Fear-Prejudice": 194,
# #     "Flag_Waving": 169,
# #     "Causal_Oversimplification": 143,
# #     "Appeal_to_Authority": 88,
# #     "Slogans": 87,
# #     "False_Dilemma-No_Choice": 81,
# #     "Conversation_Killer": 54,
# #     "Guilt_by_Association": 33,
# #     "Red_Herring": 29,
# #     "Appeal_to_Hypocrisy": 27,
# #     "Obfuscation-Vagueness-Confusion": 12,
# #     "Straw_Man": 12,
# #     "Whataboutism": 12,
# #     "Appeal_to_Popularity": 10
# # }

# # discourse_relations = {
# #     "Cause": 629,
# #     "Contrast": 466,
# #     "Cause+Belief": 355,
# #     "Concession": 251,
# #     "Instantiation": 154,
# #     "Conjunction": 131,
# #     "Condition": 120,
# #     "Asynchronous": 113,
# #     "Cause+Speechact": 112,
# #     "Purpose": 107,
# #     "Level-of-detail": 58,
# #     "Similarity": 34,
# #     "Equivalence": 29,
# #     "Disjunction": 24,
# #     "Synchronous": 15,
# #     "Substitution": 11,
# #     "Exception": 4,
# #     "Condition+Speechact": 2
# # }

# # def format_label(label):
# #     return label.replace("_", " ").replace("-", ", ")

# # # Sorting data
# # sorted_persuasion = dict(sorted(persuasion_techniques.items(), key=lambda x: x[1], reverse=True))
# # sorted_discourse = dict(sorted(discourse_relations.items(), key=lambda x: x[1], reverse=True))

# # # Format labels only for persuasion techniques
# # formatted_persuasion_keys = [format_label(k) for k in sorted_persuasion.keys()]
# # formatted_discourse_keys = list(sorted_discourse.keys())  # Keep DR relations as they are

# # # Creating subplots (stacked vertically) with more space between them
# # fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 18), sharex=True, gridspec_kw={'hspace': 0.1})

# # # Plot persuasion techniques
# # bars_persuasion = axes[0].barh(formatted_persuasion_keys, list(sorted_persuasion.values()), color="lightcoral")
# # axes[0].set_title("Persuasion Techniques")

# # # Add labels to bars in upper subplot (Persuasion Techniques)
# # for bar in bars_persuasion:
# #     width = bar.get_width()
# #     axes[0].text(width + 5, bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center')

# # axes[0].invert_yaxis()  # Invert y-axis to match order

# # # Plot discourse relations
# # bars_discourse = axes[1].barh(formatted_discourse_keys, list(sorted_discourse.values()), color="skyblue")
# # axes[1].set_title("Discourse Relations")
# # axes[1].set_xlabel("Count")  # X-axis label for lower subplot only

# # # Add labels to bars in lower subplot (Discourse Relations)
# # for bar in bars_discourse:
# #     width = bar.get_width()
# #     axes[1].text(width + 5, bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center')

# # axes[1].invert_yaxis() 

# # # Adjust layout
# # plt.tight_layout()
# # plt.savefig('Distribution_of_Persuasion_Techniques_and_Discourse_Relations_in_Silver_Dataset_(Agreement ≥5)".png')
# # plt.show()




# import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  # Import ticker for integer formatting

# # Define Silver-5
# # persuasion_techniques = {
# #     "Loaded_Language": 373,
# #     "Name_Calling-Labeling": 362,
# #     "Repetition": 333,
# #     "Doubt": 309,
# #     "Exaggeration-Minimisation": 287,
# #     "Appeal_to_Fear-Prejudice": 194,
# #     "Flag_Waving": 169,
# #     "Causal_Oversimplification": 143,
# #     "Appeal_to_Authority": 88,
# #     "Slogans": 87,
# #     "False_Dilemma-No_Choice": 81,
# #     "Conversation_Killer": 54,
# #     "Guilt_by_Association": 33,
# #     "Red_Herring": 29,
# #     "Appeal_to_Hypocrisy": 27,
# #     "Obfuscation-Vagueness-Confusion": 12,
# #     "Straw_Man": 12,
# #     "Whataboutism": 12,
# #     "Appeal_to_Popularity": 10
# # }

# PDTB-test set
discourse_relations = {
        "Contrast": 190,
        "Concession": 138,
        "Cause": 282,
        "Conjunction": 72,
        "Cause+Speechact": 82,
        "Cause+Belief": 170,
        "Condition": 60,
        "Purpose": 69,
        "Instantiation": 54,
        "Similarity": 17,
        "Asynchronous": 57,
        "Level-of-Detail": 26,
        "Disjunction": 16,
        "Synchronous": 12,
        "Substitution": 8,
        "Equivalence": 22,
        "Exception": 4,
        "Condition+Speechact": 2
    }




# persuasion_techniques = {
#     "Loaded_Language": 1809,
#     "Name_Calling-Labeling": 979,
#     "Repetition": 544,
#     "Doubt": 518,
#     "Exaggeration-Minimisation": 466,
#     "Appeal_to_Fear-Prejudice": 310,
#     "Flag_Waving": 287,
#     "Causal_Oversimplification": 213,
#     "Appeal_to_Authority": 154,
#     "Slogans": 153,
#     "False_Dilemma-No_Choice": 122,
#     "Conversation_Killer": 91,
#     "Guilt_by_Association": 59,
#     "Red_Herring": 44,
#     "Appeal_to_Hypocrisy": 40,
#     "Obfuscation-Vagueness-Confusion": 18,
#     "Whataboutism": 16,
#     "Appeal_to_Popularity": 15,
#     "Straw_Man": 15
# }
# # Silver-5
# # discourse_relations = {


# #     "Cause": 629,
# #     "Contrast": 466,
# #     "Cause+Belief": 355,
# #     "Concession": 251,
# #     "Instantiation": 154,
# #     "Conjunction": 131,
# #     "Condition": 120,
# #     "Asynchronous": 113,
# #     "Cause+Speechact": 112,
# #     "Purpose": 107,
# #     "Level-of-detail": 58,
# #     "Similarity": 34,
# #     "Equivalence": 29,
# #     "Disjunction": 24,
# #     "Synchronous": 15,
# #     "Substitution": 11,
# #     "Exception": 4,
# #     "Condition+Speechact": 2
# # }


# discourse_relations = {
#         "Contrast": 166,
#         "Concession": 133,
#         "Cause": 271,
#         "Conjunction": 68,
#         "Cause+Speechact": 67,
#         "Condition": 57,
#         "Purpose": 67,
#         "Instantiation": 49,
#         "Cause+Belief": 145,
# #         "Similarity": 17,
# #         "Asynchronous": 57,
# #         "Disjunction": 13,
# #         "Synchronous": 12,
# #         "Substitution": 8,
# #         "Level-of-Detail": 22,
# #         "Equivalence": 22,
# #         "Exception": 4,
# #         "Condition+Speechact": 1
# #     }
# persuasion_techniques= {
#     "Conjunction" :      13150,
#     "Cause":          7716,
#     "Concession":        6269,
#     "Level-of-Detail" :    3489,
#     "Asynchronous"   :    3372,
#     "Synchronous"  :     2490,
#     "Contrast"    :     1973,
#     "Instantiation"  :    1797,
#     "Purpose"     :    1766,
#     "Condition"   :     1600,
#     "Substitution" :      585,
#     "Manner"      :    512,
#     "Equivalence" :       361,
#     "Disjunction"   :     334,
#     "Cause+Belief" :     229,
#     "Similarity"   :     134,
#     "Negative-Condition" :  124,
#     "Condition+SpeechAct" :  75,
#     "Exception"  :       41,
#     "Concession+SpeechAct"  :  26,
#     "Cause+SpeechAct " : 24
# }

persuasion_techniques ={
        "Doubt": 189,
        "Appeal to Fear/Prejudice": 86,
        "Appeal to Authority": 40,
        "Slogans": 39,
        "Loaded Language": 202,
        "Name Calling/Labeling": 174,
        "Causal Oversimplification": 64,
        "Exaggeration/Minimisation": 129,
        "Repetition": 152,
        "Conversation Killer": 22,
        "False Dilemma/No Choice": 38,
        "Appeal to Popularity": 7,
        "Flag Waving": 83,
        "Appeal to Hypocrisy": 12,
        "Guilt by Association": 14,
        "Obfuscation/Vagueness/Confusion": 7,
        "Whataboutism": 7,
        "Red Herring": 12,
        "Straw Man": 4
    }

# persuasion_techniques = {
#         "Doubt": 163,
#         "Appeal_to_Fear-Prejudice": 84,
#         "Appeal_to_Authority": 38,
#         "Slogans": 38,
#         "Loaded_Language": 190,
#         "Name_Calling-Labeling": 158,
#         "Causal_Oversimplification": 61,
#         "Exaggeration-Minimisation": 122,
#         "Repetition": 145,
#         "False_Dilemma-No_Choice": 36,
#         "Appeal_to_Popularity": 7,
#         "Flag_Waving": 71,
#         "Conversation_Killer": 17,
#         "Appeal_to_Hypocrisy": 9,
#         "Guilt_by_Association": 13,
#         "Obfuscation-Vagueness-Confusion": 7,
#         "Whataboutism": 5,
#         "Red_Herring": 11,
#         "Straw_Man": 4
#     }

print(sum(persuasion_techniques.values()))

def format_label(label):
    return label.replace("_", " ").replace("-", ", ")

# Sorting data
sorted_persuasion = dict(sorted(persuasion_techniques.items(), key=lambda x: x[1], reverse=True))
sorted_discourse = dict(sorted(discourse_relations.items(), key=lambda x: x[1], reverse=True))

# Format labels
formatted_persuasion_keys = [format_label(k) for k in sorted_persuasion.keys()]
formatted_discourse_keys = list(sorted_discourse.keys())  # Keep DR relations as they are

# Creating subplots **SIDE BY SIDE**
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(24, 12), sharey=False, gridspec_kw={'wspace': 0.25})

# Adjust X-axis limits to provide more space for annotations
max_persuasion = max(sorted_persuasion.values())
max_discourse = max(sorted_discourse.values())

# Plot persuasion techniques
bars_persuasion = axes[0].barh(formatted_persuasion_keys, list(sorted_persuasion.values()), color="#F08080") 
# skyblue "lightcoral"
axes[0].set_title("Persuasion Techniques", fontsize=17)
axes[0].set_xlabel("Count", fontsize=17)
axes[0].set_xlim([0, max_persuasion * 1.13])  # Extend limit by 20%

# Add labels to bars (Persuasion Techniques)
for bar in bars_persuasion:
    width = bar.get_width()
    axes[0].text(width + (max_persuasion * 0.05), bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center', fontsize=15)

axes[0].invert_yaxis()  # Invert y-axis to match order

# Plot discourse relations
bars_discourse = axes[1].barh(formatted_discourse_keys, list(sorted_discourse.values()), color="skyblue")
axes[1].set_title("Discourse Relations", fontsize=17)
axes[1].set_xlabel("Count", fontsize=17)
axes[1].set_xlim([0, max_discourse * 1.13])  # Extend limit by 20%

axes[1].xaxis.set_major_locator(mticker.MaxNLocator(integer=True))


# Add labels to bars (Discourse Relations)
for bar in bars_discourse:
    width = bar.get_width()
    axes[1].text(width + (max_discourse * 0.05), bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center', fontsize=15)


axes[1].invert_yaxis()
# Increase y-axis label size
axes[0].tick_params(axis='y', labelsize=12)  # Persuasion Techniques
axes[1].tick_params(axis='y', labelsize=12.5)  # Discourse Relations
# Adjust layout
plt.tight_layout()
plt.savefig('Persuasion_Techniques_vs_Discourse_Relations_filtered.png')
plt.show()


