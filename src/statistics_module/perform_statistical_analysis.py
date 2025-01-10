import os
from collections import Counter
import pandas as pd
import json
import numpy as np
from scipy.stats import fisher_exact
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt


def perform_statistical_analysis():
    print('Start statistical analysis')
    data_path = os.path.join('..', 'results', 'stage2_DR_parsing_PT_annotated_semeval_datasets', '03_pooled_datasets')
    stat_result_path = os.path.join('..', 'results', 'statistical_analysis')
    contingency_path  = os.path.join(stat_result_path, 'contingency_tables' )  
    json_files = sorted([file for file in os.listdir(data_path) if file.endswith('.json')])

    threshold = 24
    global_significance_table = pd.DataFrame()  # Initialize an empty DataFrame for tracking significant results globally

    for json_file in json_files:
        fisher_results = []
        json_path = os.path.join(data_path, json_file)
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

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

        # Construct frequency table
        unique_pts = list(set(pt for (pt, _) in cooccurrence_freq_dict.keys()))
        unique_drs = list(set(dr for (_, dr) in cooccurrence_freq_dict.keys()))
        total_cooccurrences = sum(cooccurrence_freq_dict.values())

        freq_table = pd.DataFrame(0, index=unique_pts, columns=unique_drs)

        for (pt, dr), freq in cooccurrence_freq_dict.items():
            freq_table.loc[pt, dr] = freq

        freq_table=freq_table[freq_table.sum(axis=1)>threshold]
        freq_table = freq_table.loc[:, freq_table.sum(axis=0) >threshold]

        freq_table['Row_Sum'] = freq_table.sum(axis=1)
        freq_table.loc['Col_Sum'] = freq_table.sum(axis=0)

        # PPMI
        ppmi_table = pd.DataFrame(0.0, index=freq_table.index[:-1], columns= freq_table.columns[:-1])
        for pt in ppmi_table.index:
            for dr in ppmi_table.columns:
                # calculate frequencies
                pt_freq = pt_freq_dict[pt]
                dr_freq = dr_freq_dict[dr]
                pt_dr_freq = cooccurrence_freq_dict.get((pt, dr), 0)

                # calculate probabilities
                p_pt = pt_freq / total_cooccurrences if total_cooccurrences else 0
                p_dr = dr_freq / total_cooccurrences if total_cooccurrences else 0
                p_pt_dr = pt_dr_freq / total_cooccurrences if total_cooccurrences else 0

                # calculate PPMI
                if p_pt_dr and (p_pt * p_dr > 0):
                    ppmi_value = max(0, np.log2(p_pt_dr / (p_pt * p_dr)))
                else:
                    ppmi_value = 0
                ppmi_table.loc[pt, dr] = ppmi_value

        path = os.path.join(contingency_path, f'{json_file}.txt')
        with open(path, 'a') as f:
            f.write(f'_______________\nPooling: {json_file}\n______________\n')
        # Create binary contingency tables and perform Fisher's Exact Test
        for pt in freq_table.index[:-1]:  # Ignore the Row_Sum row
            for dr in freq_table.columns[:-1]:  # Ignore the Col_Sum column
                a = freq_table.loc[pt, dr]
                b = freq_table.loc[pt, 'Row_Sum'] - a
                c = freq_table.loc['Col_Sum', dr] - a
                d = total_cooccurrences - (a + b + c)

                contingency_table = np.array([[a, b], [c, d]])
                odds_ratio, p_value = fisher_exact(contingency_table, alternative='two-sided')
                
                if odds_ratio > 1 and p_value < 0.05:
                    pair = f"{pt} || {dr}" 
                    global_significance_table.loc[pair, json_file] = '+'

                fisher_results.append({
                    'PT': pt,
                    'DR': dr,
                    'Odds_Ratio': odds_ratio,
                    'P_Value': p_value
                })

                table_str = (
                    f"Contingency Table for {pt} || {dr}:\n"
                    f"              DR Present  DR Absent\n"
                    f"PT Present    {a:<12} {b:<10}\n"
                    f"PT Absent     {c:<12} {d:<10}\n\n"
                )

                with open(path, 'a') as f:
                    f.write(f'{table_str}\n')

        # Prepare Heatmap DataFrame
        heatmap_df_p_value = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])   # Exclude Row_Sum and Col_Sum
        heatmap_df_OR = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])   # Exclude Row_Sum and Col_Sum
        heatmap_df_both = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])   # Exclude Row_Sum and Col_Sum

        for result in fisher_results:
            pt, dr = result['PT'], result['DR']
            heatmap_df_p_value.loc[pt, dr] = result['P_Value']
            heatmap_df_OR.loc[pt, dr] = result['Odds_Ratio']
            # heatmap_df_both.loc[pt, dr] = '+' if result['Odds_Ratio'] > 1 and result['P_Value'] < 0.05 else 'NA'
            heatmap_df_both.loc[pt, dr] = f'({round(result['P_Value'], 3)}, {round(result['Odds_Ratio'],1)})' if result['Odds_Ratio'] > 1 and result['P_Value'] < 0.05 else ''

        # PT-PT cosine similarity
        pt_vectors = ppmi_table.values
        pt_labels = ppmi_table.index
        pt_cos_similarity = cosine_similarity(pt_vectors)
        pt_cos_similarity_df = pd.DataFrame(pt_cos_similarity, index=pt_labels, columns=pt_labels)

        # PT-PT cos similarity heatmaps
        plt.figure(figsize=(12,10))
        plt.title(f"Cosine Similarity Between PTs ({json_file})")
        sns.heatmap(pt_cos_similarity_df, annot=True, cmap='coolwarm', cbar=True)
        path = os.path.join(stat_result_path, 'cosine_similarities', f'heatmap_pt_cosine_sim_{json_file}.png')
        plt.tight_layout()
        plt.savefig(path)
        plt.close()  

        # save files
        path = os.path.join(stat_result_path, 'freq_tables', f'freq_table_{json_file}.xlsx')
        freq_table.to_excel(path)  

        path = os.path.join(stat_result_path, 'ppmi_tables', f'ppmi_table_{json_file}.xlsx')
        ppmi_table.to_excel(path)  

        fisher_results_df = pd.DataFrame(fisher_results)
        path = os.path.join(stat_result_path, 'fisher_results', f'fisher_results_{json_file}.xlsx')
        fisher_results_df.to_excel(path)

        path = os.path.join(stat_result_path, 'heatmap_data', f'p_value_{json_file}.xlsx')
        heatmap_df_p_value.to_excel(path)

        path = os.path.join(stat_result_path, 'heatmap_data', f'OR_{json_file}.xlsx')
        heatmap_df_OR.to_excel(path)

        path = os.path.join(stat_result_path, 'heatmap_data', f'significant_positive_results_{json_file}.xlsx')
        heatmap_df_both.to_excel(path)

        path = os.path.join(stat_result_path, 'cosine_similarities', f'pt_cosine_sim_{json_file}.xlsx')
        pt_cos_similarity_df.to_excel(path)

    # Save the final global table
    global_significance_table = global_significance_table.sort_index(axis=1)
    global_significance_table = global_significance_table.sort_index(axis=0)
    output_path = os.path.join(stat_result_path, 'global_significant_results.xlsx')
    global_significance_table.to_excel(output_path)

    # Print summary for this file
    print(f"- Frequency table saved to: {os.path.join(stat_result_path, 'freq_tables')}")
    print(f"- PPMI table saved to: {os.path.join(stat_result_path, 'ppmi_tables')}")
    print(f"- Fisher results saved to: {os.path.join(stat_result_path, 'fisher_results')}")
    print(f"- Heatmap p-value data saved to: {os.path.join(stat_result_path, 'heatmap_data')}")
    print(f"- Heatmap OR data saved to: {os.path.join(stat_result_path, 'heatmap_data')}")
    print(f"- Heatmap significant positive results data saved to: {os.path.join(stat_result_path, 'heatmap_data')}")
    print(f"- PT cosine similarity heatmap saved to: {os.path.join(stat_result_path, 'cosine_similarities')}")









        







