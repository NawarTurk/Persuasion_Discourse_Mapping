import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from collections import Counter
import numpy as np


stat_result_path = os.path.join('..', 'results', 'stage3_statistical_analysis')




def draw_pt_dr_association_heatmap(global_significance_pairs_dict):
    output_path = os.path.join('..', 'results', 'stage3_statistical_analysis','pt_dr_association_heatmap')
    
    
    
    dr_mapping = {
        'cause': 'Cause',
        'contrast': 'Contrast',
        'cause+speechact': 'Cause+Speechact',
        'concession': 'Concession',
        'cause+belief': 'Cause+Belief',
        'instantiation': 'Instantiation',
        'condition': 'Condition',
        'asynchronous': 'Asynchronous',
        'purpose': 'Purpose',
        'level-of-detail': 'Level-of-Detail'
    }
    pt_mapping = {
        'Appeal_to_Authority': 'Appeal to Authority',
        'Appeal_to_Fear-Prejudice': 'Appeal to Fear/Prejudice',
        'Causal_Oversimplification': 'Causal Oversimplification',
        'Doubt': 'Doubt',
        'Slogans': 'Slogans',
        'Exaggeration-Minimisation': 'Exaggeration/Minimisation',
        'False_Dilemma-No_Choice': 'False Dilemma/No Choice',
        'Flag_Waving': 'Flag Waving',
        'Loaded_Language': 'Loaded Language',
        'Name_Calling-labeling': 'Name Calling/Labeling',
        'Repetition': 'Repetition'
    }


    global_significance_pairs_list = [
        {'pt': key[0],'dr': key[1], 'pooling_techniques': value['pooling_techniques'], 'P_DR_given_PT': value['P_DR_given_PT']} for key, value in global_significance_pairs_dict.items()
    ]
    global_significance_pairs_df = pd.DataFrame(global_significance_pairs_list)
    global_significance_pairs_df['pooling_techniques_count'] = global_significance_pairs_df['pooling_techniques'].apply(len)
    global_significance_pairs_df['P_DR_given_PT_average1'] = global_significance_pairs_df['P_DR_given_PT'].apply(
        lambda x: round(np.mean(x),2) if len(x) > 0 else 0
        )

    global_significance_pairs_df = global_significance_pairs_df.sort_values(by='pooling_techniques_count', ascending=False)
   

    # Create a copy for the heatmap
    heatmap_df = global_significance_pairs_df.copy()

    # # # Apply mappings to the copy
    heatmap_df['dr'] = heatmap_df['dr'].map(dr_mapping)
    heatmap_df['pt'] = heatmap_df['pt'].map(pt_mapping)

    # Create pivot table
    heatmap_data = pd.pivot_table(
        heatmap_df,
        values='pooling_techniques_count',
        index='pt',
        columns='dr',
        fill_value=0
    )

    # Define custom orders
    custom_dr_order = [
        'Cause',       
        'Purpose',   
        'Contrast',
        'Cause+Belief',    
        'Concession', 
        'Condition',       
        'Cause+Speechact',     
        'Instantiation',  
        'Asynchronous',    
        'Level-of-Detail',
    ]

    custom_pt_order = [
        'Slogans',
        'Appeal to Authority',
        'False Dilemma/No Choice',
        'Loaded Language',
        'Appeal to Fear/Prejudice',
        'Causal Oversimplification',
        'Flag Waving',
        'Doubt',
        'Name Calling/Labeling',
        'Repetition',
        'Exaggeration/Minimisation',

    ]

    # Filter to keep only existing columns and rows
    existing_dr_order = [dr for dr in custom_dr_order if dr in heatmap_data.columns]
    existing_pt_order = [pt for pt in custom_pt_order if pt in heatmap_data.index]

    # # # # # Reorder both columns and rows
    heatmap_data = heatmap_data[existing_dr_order]
    heatmap_data = heatmap_data.reindex(existing_pt_order)

    # Create the heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        heatmap_data,
        annot=True,
        cmap='Greens',
        annot_kws={'size': 13},
        cbar_kws={
        'label': 'Number of Silver Datasets with Significant Association for that Pair\n(Fisher p <= 0.05, OR > 1)',
        'ticks': range(6),  # Assuming your data goes from 0 to 5
        'format': '%d'  # For integer values
    }

    )
    ax = plt.gca()
    colorbar = ax.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=13)  # Increase the size of the numbers
    plt.xlabel("DR", fontsize=14)
    plt.ylabel("PT", fontsize=14)
    plt.xticks(fontsize=13)  # Increase x-axis tick size
    plt.yticks(fontsize=13)  # Increase y-axis tick size
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

def create_freq_table(data, freq_threshold):

    # Calculate frequencies
    dr_freq_dict = Counter()
    pt_freq_dict = Counter()
    cooccurrence_freq_dict = Counter()
    for item in data.values():
        dr = item['DR']
        pt = item['PT']
        dr_freq_dict[dr] += 1
        pt_freq_dict[pt] += 1
        cooccurrence_freq_dict[(pt,dr)] += 1

    unique_pts = list(set(pt for (pt, _) in cooccurrence_freq_dict.keys()))
    unique_drs = list(set(dr for (_, dr) in cooccurrence_freq_dict.keys()))
    total_cooccurrences = sum(cooccurrence_freq_dict.values())

    freq_table = pd.DataFrame(0, index=unique_pts, columns=unique_drs)

    for (pt, dr), freq in cooccurrence_freq_dict.items():
        freq_table.loc[pt, dr] = freq

    freq_table=freq_table[freq_table.sum(axis=1)>freq_threshold]
    freq_table = freq_table.loc[:, freq_table.sum(axis=0) >freq_threshold]

    freq_table['Row_Sum'] = freq_table.sum(axis=1)
    freq_table.loc['Col_Sum'] = freq_table.sum(axis=0)

    return(freq_table, dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict, total_cooccurrences)

def save_sorted_global_sig_table(global_significance_table): 
    global_significance_table.copy()
    global_significance_table = global_significance_table.sort_index(axis=1)
    global_significance_table = global_significance_table.sort_index(axis=0)
    output_path = os.path.join(stat_result_path, 'global_significant_result_table.xlsx')
    global_significance_table.to_excel(output_path)

def save_pt_dr_ppmi_heatmap(ppmi_table, json_file):
        plt.figure(figsize=(12,10))
        plt.title(f"PT DR PPMI ({json_file})")
        sns.heatmap(ppmi_table, annot=True, cmap='Greens', cbar=True)
        plt.tight_layout()
        path = os.path.join(stat_result_path, 'pt_dr_ppmi_tables', f'ppmi_heatmap_{json_file}.png')
        plt.savefig(path)
        plt.close()  

def create_global_ppmi_heatmap(ppmi_global_table):

    output_path = os.path.join(stat_result_path, 'pt_dr_ppmi_tables', 'global_ppmi_table.xlsx')
    ppmi_global_table.round(2).to_excel(output_path)

    ppmi_global_table = ppmi_global_table.astype(float)
    plt.figure(figsize=(12,10))
    plt.title("Global Average PPMI Across Datasets")
    sns.heatmap(ppmi_global_table.round(2), 
                annot=True, 
                cmap='Greens', 
                cbar=True,
                fmt='.2f',
                annot_kws={"fontsize": 10})
    plt.tight_layout()
    path = os.path.join(stat_result_path, 'pt_dr_ppmi_tables', 'global_ppmi_heatmap.png')
    plt.savefig(path)
    plt.close()