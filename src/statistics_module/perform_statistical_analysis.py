import os
import pandas as pd
import json
import numpy as np
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt
from collections import defaultdict

from statistics_module.helper_methos import draw_pt_dr_association_heatmap, create_freq_table, create_global_ppmi_heatmap, save_sorted_global_sig_table, save_pt_dr_ppmi_heatmap


def perform_statistical_analysis():
    print('Start statistical analysis')
    data_path = os.path.join('..','results', 'stage2_DR_parsing_of_PT_annotated_semeval_datasets', '03_pooled_datasets')
    stat_result_path = os.path.join('..', 'results', 'stage3_statistical_analysis')
    contingency_path  = os.path.join(stat_result_path, 'pt_dr_contingency_tables' )  
    json_files = sorted([file for file in os.listdir(data_path) if file.endswith('.json')])
    
    freq_threshold = 24
    conditional_probability_threshold = 0
    OR_threshold = 1
    p_value_threshold = 0.05


    global_significance_table = pd.DataFrame()  # Initialize an empty DataFrame for tracking significant results globally
    global_significance_pairs_dict = defaultdict(lambda: {'p_value': None, 'odds_ratio': None, 'P_DR_given_PT': None, 'pooling_techniques': [], 'P_DR_given_PT': []})

    ppmi_global_table = pd.DataFrame()  
    ppmi_count_global_table = pd.DataFrame()   


    for json_file in json_files:
        json_file = json_file[:-5]
        all_metric_results = []
        json_path = os.path.join(data_path, os.path.join(f'{json_file}.json'))
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        freq_table, dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict,  total_cooccurrences =  create_freq_table(data, freq_threshold)


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

                # update the golbal ppmi table
                if ppmi_global_table.empty:
                    # First insertion - create table with both pt and dr
                    ppmi_global_table = pd.DataFrame(index=[pt], columns=[dr])
                    ppmi_count_global_table = pd.DataFrame(index=[pt], columns=[dr])
                    ppmi_global_table.loc[pt, dr] = ppmi_value
                    ppmi_count_global_table.loc[pt, dr] = 1
                else:
                    if pt not in ppmi_global_table.index:
                        ppmi_global_table.loc[pt] = pd.Series(0.0, index=ppmi_global_table.columns)
                        ppmi_count_global_table.loc[pt] = pd.Series(0.0, index=ppmi_count_global_table.columns)
                    if dr not in ppmi_global_table.columns:
                        ppmi_global_table[dr] = pd.Series(0.0, index=ppmi_global_table.index)
                        ppmi_count_global_table[dr] = pd.Series(0.0, index=ppmi_count_global_table.index)

                current_global_ppmi_avg = ppmi_global_table.loc[pt, dr]
                current_global_ppmi_count = ppmi_count_global_table.loc[pt, dr]

                ppmi_global_table.loc[pt,dr] = ((current_global_ppmi_avg*current_global_ppmi_count) + ppmi_value)/(current_global_ppmi_count+1)
                ppmi_count_global_table.loc[pt, dr] += 1
        ppmi_table = ppmi_table.round(2)

        
        save_pt_dr_ppmi_heatmap(ppmi_table, json_file)
    

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
                    'P_DR_given_PT': float(P_DR_given_PT)
                })

                table_str = (
                    f"Contingency Table for {pt} || {dr}:\n"
                    f"              DR Present  DR Absent\n"
                    f"PT Present    {a:<12} {b:<10}\n"
                    f"PT Absent     {c:<12} {d:<10}\n\n"
                )

                with open(path, 'a') as f:
                    f.write(f'{table_str}\n')

        # The three metric dataframes (p value, odds ratio, conditional probability)
        p_values_df = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])   # Exclude Row_Sum and Col_Sum
        OR_values_df  = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])   # Exclude Row_Sum and Col_Sum
        conditional_probability_df = pd.DataFrame(index=freq_table.index[:-1], columns=freq_table.columns[:-1])

        # Positively associated dataframe
        df = pd.DataFrame(all_metric_results)
        positively_associated_pairs_df = df[(df['P_Value'] <= p_value_threshold) & (df['Odds_Ratio'] > OR_threshold) & (df['P_DR_given_PT'] >= conditional_probability_threshold)]
       


 
        
        # Contributing to global calculations
        # * global_significance_pairs_dict
        for result in all_metric_results:
            pt, dr = result['PT'], result['DR']
            p_value, odds_ratio, P_DR_given_PT =  result['P_Value'], result['Odds_Ratio'], result['P_DR_given_PT']
            p_values_df.loc[pt, dr] = p_value
            OR_values_df.loc[pt, dr] = odds_ratio
            conditional_probability_df.loc[pt, dr] = P_DR_given_PT
            if result['P_Value'] <= p_value_threshold and result['Odds_Ratio'] > OR_threshold and P_DR_given_PT >= conditional_probability_threshold:
                key = (pt, dr)
                # global_significance_pairs_dict[key]['p_value'] = p_value
                # global_significance_pairs_dict[key]['Odds_Ratio'] = odds_ratio
                global_significance_pairs_dict[key]['P_DR_given_PT'].append(P_DR_given_PT)
                global_significance_pairs_dict[key]['pooling_techniques'].append(json_file)

 

        # save frequencey table
        path = os.path.join(stat_result_path, 'pt_dr_freq_tables', f'freq_table_{json_file}.xlsx')
        freq_table.to_excel(path)  

        # save PT DR PPMI tables
        path = os.path.join(stat_result_path, 'pt_dr_ppmi_tables', f'ppmi_table_{json_file}.xlsx')
        ppmi_table.to_excel(path)  

  
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


    save_sorted_global_sig_table(global_significance_table)
    draw_pt_dr_association_heatmap(global_significance_pairs_dict)
    create_global_ppmi_heatmap(ppmi_global_table)
  


