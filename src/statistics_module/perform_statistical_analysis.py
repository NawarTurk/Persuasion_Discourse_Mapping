import os
from collections import Counter
import pandas as pd
import json
import numpy as np
from scipy.stats import fisher_exact
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


def perform_statistical_analysis():
    print('Start statistical analysis')
    data_path = os.path.join('..','results', 'stage2_DR_parsing_of_PT_annotated_semeval_datasets', '03_pooled_datasets')
    stat_result_path = os.path.join('..', 'results', 'stage3_statistical_analysis')
    contingency_path  = os.path.join(stat_result_path, 'pt_dr_contingency_tables' )  
    json_files = sorted([file for file in os.listdir(data_path) if file.endswith('.json')])
    
    freq_threshold = 24
    cos_sim_threshold = 0.7
    conditional_probability_threshold = 0.2
    OR_threshold = 1
    p_value_threshold = 0.05


    global_significance_table = pd.DataFrame()  # Initialize an empty DataFrame for tracking significant results globally
    global_significance_pairs_dict = defaultdict(lambda: {'p_value': None, 'odds_ratio': None, 'P_DR_given_PT': None, 'pooling_techniques': []})
    global_cos_similarity_df = pd.DataFrame()

    for json_file in json_files:
        json_file = json_file[:-5]
        all_metric_results = []
        json_path = os.path.join(data_path, os.path.join(f'{json_file}.json'))
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

        freq_table=freq_table[freq_table.sum(axis=1)>freq_threshold]
        freq_table = freq_table.loc[:, freq_table.sum(axis=0) >freq_threshold]

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

        

        # PT-DR PPMI heatmaps ______________________________________________________check all titlews
        plt.figure(figsize=(12,10))
        plt.title(f"PT DR PPMI ({json_file})")
        sns.heatmap(ppmi_table, annot=True, cmap='Greens', cbar=True)
        plt.tight_layout()
        path = os.path.join(stat_result_path, 'pt_dr_ppmi_tables', f'ppmi_heatmap_{json_file}.png')
        plt.savefig(path)
        plt.close()  

        path = os.path.join(contingency_path, f'contingency_tables_{json_file}.txt')
        with open(path, 'a') as f:
            f.write(f'_______________\nPooling: {json_file}\n______________\n')

        # Create binary contingency tables and perform Fisher's Exact Test
        for pt in freq_table.index[:-1]:  # Ignore the Row_Sum row
            for dr in freq_table.columns[:-1]:  # Ignore the Col_Sum column
                a = freq_table.loc[pt, dr]
                b = freq_table.loc[pt, 'Row_Sum'] - a
                c = freq_table.loc['Col_Sum', dr] - a
                d = total_cooccurrences - (a + b + c)

                # calculate metrics
                contingency_table = np.array([[a, b], [c, d]])
                odds_ratio, p_value = fisher_exact(contingency_table, alternative='two-sided')
                P_DR_given_PT = a / (a + b) if (a + b) > 0 else 0  # P(DR | PT)

                pair = f"{pt} || {dr}" 
                if odds_ratio > OR_threshold and p_value < p_value_threshold and P_DR_given_PT >= conditional_probability_threshold:
                    global_significance_table.loc[pair, json_file] = '+'

                all_metric_results.append({
                    'PT': pt,
                    'DR': dr,
                    'Odds_Ratio': odds_ratio,
                    'P_Value': p_value,
                    'P_DR_given_PT': P_DR_given_PT
                })

                table_str = (
                    f"Contingency Table for {pt} || {dr}:\n"
                    f"              DR Present  DR Absent\n"
                    f"PT Present    {a:<12} {b:<10}\n"
                    f"PT Absent     {c:<12} {d:<10}\n\n"
                )

                with open(path, 'a') as f:
                    f.write(f'{table_str}\n')

        # The three metric dataframes
        p_values_df = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])   # Exclude Row_Sum and Col_Sum
        OR_values_df  = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])   # Exclude Row_Sum and Col_Sum
        conditional_probability_df = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])

        # Positively associated dataframe
        df = pd.DataFrame(all_metric_results)
        positively_associated_pairs_df = df[(df['P_Value'] <= p_value_threshold) & (df['Odds_Ratio'] > OR_threshold) & (df['P_DR_given_PT'] >= conditional_probability_threshold)]
       
        # PT-PT cosine similarity dataframe
        pt_vectors = ppmi_table.values
        pt_labels = ppmi_table.index
        pt_cos_similarity = cosine_similarity(pt_vectors)
        pt_cos_similarity_df = pd.DataFrame(pt_cos_similarity, index=pt_labels, columns=pt_labels)

        # PT-PT cos similarity heatmaps
        plt.figure(figsize=(12,10))
        plt.title(f"Cosine Similarity Between PTs ({json_file})")
        sns.heatmap(pt_cos_similarity_df, annot=True, cmap='Greens', cbar=True)
        plt.tight_layout()
        path = os.path.join(stat_result_path, 'cosine_similarities', f'heatmap_pt_cosine_sim_{json_file}.png')
        plt.savefig(path)
        plt.close()  
        
        # Contributing to global calculations
        for result in all_metric_results:
            pt, dr = result['PT'], result['DR']
            p_value, odds_ratio, P_DR_given_PT =  result['P_Value'], result['Odds_Ratio'], result['P_DR_given_PT']
            p_values_df.loc[pt, dr] = p_value
            OR_values_df.loc[pt, dr] = odds_ratio
            conditional_probability_df.loc[pt, dr] = P_DR_given_PT
            if result['P_Value'] <= p_value_threshold and result['Odds_Ratio'] > OR_threshold and P_DR_given_PT >= conditional_probability_threshold:
                key = (pt, dr)
                global_significance_pairs_dict[key]['p_value'] = p_value
                global_significance_pairs_dict[key]['Odds_Ratio'] = odds_ratio
                global_significance_pairs_dict[key]['P_DR_given_PT'] = P_DR_given_PT
                if json_file not in global_significance_pairs_dict[key]['pooling_techniques']:
                    global_significance_pairs_dict[key]['pooling_techniques'].append(json_file)

        for index in pt_cos_similarity_df.index:
            for col in pt_cos_similarity_df.columns:
                value = pt_cos_similarity_df.at[index, col]
                if value >= cos_sim_threshold and index != col:
                    pair = f'{index}||{col}'
                    global_cos_similarity_df.loc[pair, json_file] = '+'



        # save frequencey table
        path = os.path.join(stat_result_path, 'pt_dr_freq_tables', f'freq_table_{json_file}.xlsx')
        freq_table.to_excel(path)  

        # save PT DR PPMI table
        path = os.path.join(stat_result_path, 'pt_dr_ppmi_tables', f'ppmi_table_{json_file}.xlsx')
        ppmi_table.to_excel(path)  

        path = os.path.join(stat_result_path, 'cosine_similarities', f'pt_cosine_sim_{json_file}.xlsx')
        pt_cos_similarity_df.to_excel(path)

        path = os.path.join(stat_result_path, 'significant_association_analysis', 'fisher_p_value',f'fisher_p_value_{json_file}.xlsx')
        p_values_df.to_excel(path)

        path = os.path.join(stat_result_path, 'significant_association_analysis', 'odds_ratio', f'OR_{json_file}.xlsx')
        OR_values_df.to_excel(path)

        path = os.path.join(stat_result_path, 'significant_association_analysis', 'conditional_probability', f'OR_{json_file}.xlsx')
        conditional_probability_df.to_excel(path)

        all_metric_results_df = pd.DataFrame(all_metric_results)
        path = os.path.join(stat_result_path, 'significant_association_analysis', 'all_metric_results', f'pt_dr_association_analysis_{json_file}.xlsx')
        all_metric_results_df.to_excel(path)

        path = os.path.join(stat_result_path, 'significant_association_analysis', 'significant_positive_association', f'significant_positive_results_{json_file}.xlsx')
        positively_associated_pairs_df.to_excel(path)


# _________

    global_significance_pairs_list = [
        {'pt': key[0],'dr': key[1], 'pooling_techniques': value['pooling_techniques']} for key, value in global_significance_pairs_dict.items()
    ]
    global_significance_pairs_df = pd.DataFrame(global_significance_pairs_list)
    global_significance_pairs_df['pooling_techniques_count'] = global_significance_pairs_df['pooling_techniques'].apply(len)
    global_significance_pairs_df = global_significance_pairs_df.sort_values(by='pooling_techniques_count', ascending=False)

    # Filling global cosine similarity table
    # Loop through the columns (files) in the global DataFrame
    global_cos_similarity_filled_df = global_cos_similarity_df.copy()
    for file in global_cos_similarity_df.columns:
        # Construct the path to the precomputed cosine similarity file
        cos_sim_path = os.path.join(stat_result_path, 'cosine_similarities', f'pt_cosine_sim_{file}.xlsx')
        
        # Check if the file exists before proceeding
        if os.path.exists(cos_sim_path):
            # Load the saved cosine similarity DataFrame for the current file
            pt_cos_similarity_df = pd.read_excel(cos_sim_path, index_col=0)  # Use PT labels as both row and column indices

            # Iterate over all pairs in the global DataFrame (rows)
            for pair in global_cos_similarity_df.index:
                # Extract the individual PTs from the pair (format: PT1||PT2)
                if "||" in pair:
                    pt1, pt2 = pair.split("||")
                    
                    # Check if the pair exists in the precomputed similarity DataFrame
                    if pt1 in pt_cos_similarity_df.index and pt2 in pt_cos_similarity_df.columns:
                        # Fill the global DataFrame with the cosine similarity value
                        global_cos_similarity_filled_df.loc[pair, file] = pt_cos_similarity_df.loc[pt1, pt2]           
    global_cos_similarity_filled_df = global_cos_similarity_filled_df.fillna(-0.1)


    # Save the global table
    global_significance_table = global_significance_table.sort_index(axis=1)
    global_significance_table = global_significance_table.sort_index(axis=0)
    output_path = os.path.join(stat_result_path, 'global_significant_result_table.xlsx')
    global_significance_table.to_excel(output_path)

    output_path = os.path.join(stat_result_path, 'global_significant_result_pair_list.xlsx')
    global_significance_pairs_df.to_excel(output_path, index=False)

    global_cos_similarity_df = global_cos_similarity_df.sort_index(axis=1)
    global_cos_similarity_df = global_cos_similarity_df.sort_index(axis=0)
    output_path = os.path.join(stat_result_path, 'global_cos_sim.xlsx')
    global_cos_similarity_df.to_excel(output_path)

    # Save the updated global_cos_similarity_df
    output_path = os.path.join(stat_result_path, 'global_cos_sim_filled.xlsx')
    global_cos_similarity_filled_df.to_excel(output_path)

    # Global PT-PT cos similarity heatmaps
    plt.figure(figsize=(12,10))
    plt.title(f"Global Cosine Similarity Between PTs ({json_file})")
    sns.heatmap(global_cos_similarity_filled_df, annot=True, cmap='Greens', cbar=True, vmin=cos_sim_threshold)
    plt.tight_layout()
    path = os.path.join(stat_result_path, 'heatmap_global_cos_similarity_df.png')
    plt.savefig(path)
    plt.close()  

    # Print summary for this file
    print(f"- Frequency table saved to: {os.path.join(stat_result_path, 'pt_dr_freq_tables')}")
    print(f"- PPMI table saved to: {os.path.join(stat_result_path, 'pt_dr_ppmi_tables')}")
    print(f"- Fisher results saved to: {os.path.join(stat_result_path, 'fisher_results')}")
    print(f"- Heatmap p-value data saved to: {os.path.join(stat_result_path, 'significant_association')}")
    print(f"- Heatmap OR data saved to: {os.path.join(stat_result_path, 'significant_association')}")
    print(f"- Heatmap significant positive results data saved to: {os.path.join(stat_result_path, 'heatmap_data')}")
    print(f"- PT cosine similarity heatmap saved to: {os.path.join(stat_result_path, 'cosine_similarities')}")