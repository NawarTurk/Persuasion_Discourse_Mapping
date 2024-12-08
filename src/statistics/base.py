import argparse
import os
from statistical_significance import *
from heatmap import *
from ppmi import *
from clustering import *
from probabilities import *
from tools import *
from datetime import datetime



def main():

    parser = argparse.ArgumentParser(description="Input file name, number of clusters and if verbose")
    parser.add_argument("input_file_name", type=str, help="Input file name")
    parser.add_argument("number_of_clusters", type=str, help="Number of Clusters")
    parser.add_argument("if_verbose", type=bool, help="If verbose")

    args = parser.parse_args()

    input_file = args.input_file_name
    nb_clusters = args.number_of_clusters

    data_path = f"../../dataset/mock_data"
    json_data_list = get_data_from_files(data_path)
    # print(json_data_list)

    dr_freq_dict_list = []
    pt_freq_dict_list = []
    coocurence_freq_dict_list = []
    total_count_list = []
    ppmi_df_list = []
    ppmi_filtered_df_list = []
    pt_pt_cosine_similarity_df_list = []
    fisher_p_df_list = []
    combined_p_df_list = []

    now = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
    file_name = f"statistical_analysis-{now}"

    counter = 1
    while os.path.exists(file_name):
        file_name = f"{file_name}_{counter}"
        counter += 1

    os.mkdir(file_name)
    os.chdir(file_name)

    for i in range(len(json_data_list)):

        # 1. Extract Frequencies
        dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict = extract_data_frequencies(json_data_list[i])
        dr_freq_dict_list.append(dr_freq_dict)
        pt_freq_dict_list.append(pt_freq_dict)
        coocurence_freq_dict_list.append(cooccurrence_freq_dict)

        # 2. Calculate Total Count
        total_count = sum(cooccurrence_freq_dict.values())
        total_count_list.append(total_count)

        # 3. Calculate Probabilities
        dr_prob, pt_prob, joint_prob = calculate_probabilities(dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict, total_count)

        # 4. Calculate PPMI
        ppmi = calculate_ppmi(dr_prob, pt_prob, joint_prob)

        # 5. Naive Bayes (Optional)
        nb_prob = naive_bayes(dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict)

        # 6. Compute PT Given DR (Optional)
        pt_given_dr = compute_pt_given_dr(joint_prob, dr_prob)

        # 7. Sort DRs and PTs
        dr_list = sorted(dr_freq_dict.keys())
        pt_list = sorted(pt_freq_dict.keys())

        # 8. Create PPMI DataFrame
        ppmi_df = create_ppmi_df(ppmi, dr_list, pt_list)
        ppmi_df_list.append(ppmi_df)

        # 9. Create Filtered PPMI DataFrame
        ppmi_filtered_df = create_filtered_ppmi_df(ppmi, pt_freq_dict, dr_freq_dict, pt_filter_nb=15, dr_filter_nb=10)
        ppmi_filtered_df_list.append(ppmi_filtered_df)

        # 10. Compute Cosine Similarity
        dr_cosine_similarity_df = compute_cosine_similarity(ppmi_df)
        pt_pt_cosine_similarity_df = compute_cosine_similarity(ppmi_df.T)
        pt_pt_cosine_similarity_df_list.append(pt_pt_cosine_similarity_df)

        # 11. Plot Heatmaps
        plot_pt_dr_ppmi_heatmap(ppmi_filtered_df, i)
        plot_pt_pt_cosine_similarity_heatmap(pt_pt_cosine_similarity_df, i)

        # 12. Perform Statistical Association Tests
        fisher_exact_dict, chi2_or_fisher_exact_dict = statistical_association_test(dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict, total_count)

        # 13. Convert Dictionaries to DataFrames
        fisher_p_df, fisher_x_df, combined_p_df, combined_x_df = dict_to_df(fisher_exact_dict, chi2_or_fisher_exact_dict)

        fisher_p_df_list.append(fisher_p_df)
        combined_p_df_list.append(combined_p_df)

    #
    # combined_ppmi_and_statistical_association(fisher_p_df, ppmi_df)
    # # combined_ppmi_and_statistical_association(combined_p_df, ppmi_df)
    #
    # # fisher_pivot_df = fisher_p_df.pivot(index="DR", columns="PT", values="P-Value")
    # # print(fisher_pivot_df)
    #
    #
    #
    # # for (dr, pt), (chi2_stat, p_value) in fisher_exact_dict.items():
    # #     print(f"DR: {dr}, PT: {pt} -> Chi-Squared: {chi2_stat:.4f}, p-value: {p_value:.4f}")

if __name__ == "__main__":
    main()