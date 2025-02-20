from scipy.stats import chi2_contingency
from scipy.stats import fisher_exact
from scipy.stats import chi2
import pandas as pd
import numpy as np


def chi_squared_calc(dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict, total_count):

    chi_squared_dict = {}

    # Contingency Table
    #           PT   Not PT
    # DR        A    B
    # Not DR    C    D

    for (dr, pt), freq in cooccurrence_freq_dict.items():

        A = freq
        B = dr_freq_dict[dr] - freq
        C = pt_freq_dict[pt] - freq
        D = total_count - (freq + B + C)

        contingency_table = np.array([[A, B], [C, D]])

        res = chi2_contingency(contingency_table)

        x = res.statistic
        p = res.pvalue
        dof = res.dof
        expected_freq_table = res.expected_freq

        chi_squared_dict[(dr, pt)] = [x, p, dof, expected_freq_table]

    return chi_squared_dict

def fisher_exact_calc(dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict, total_count):

    fisher_exact_dict = {}

    # Contingency Table
    #           PT   Not PT
    # DR        A    B
    # Not DR    C    D

    for (dr, pt), freq in cooccurrence_freq_dict.items():

        A = freq
        B = dr_freq_dict[dr] - freq
        C = pt_freq_dict[pt] - freq
        D = total_count - (freq + B + C)

        contingency_table = np.array([[A, B], [C, D]])

        res = fisher_exact(contingency_table)

        x = res.statistic
        p = res.pvalue

        fisher_exact_dict[(dr, pt)] = [x, p]

    return fisher_exact_dict

def statistical_association_test(dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict, total_count):

    fisher_exact_dict = {}
    chi2_or_fisher_exact_dict = {}

    for (dr, pt), freq in cooccurrence_freq_dict.items():

        A = freq
        B = dr_freq_dict[dr] - freq
        C = pt_freq_dict[pt] - freq
        D = total_count - (freq + B + C)

        contingency_table = np.array([[A, B], [C, D]])

        # print(contingency_table)

        res = chi2_contingency(contingency_table)

        chi2_x = res.statistic
        chi2_p = res.pvalue
        chi2_dof = res.dof
        chi2_expected_freq_table = res.expected_freq

        res = fisher_exact(contingency_table)

        fisher_exact_x = res.statistic
        fisher_exact_p = res.pvalue

        fisher_exact_dict[(dr, pt)] = [fisher_exact_x, fisher_exact_p]

        if (chi2_expected_freq_table < 5).any():
            chi2_or_fisher_exact_dict[(dr, pt)] = [fisher_exact_x, fisher_exact_p]
        else:
            chi2_or_fisher_exact_dict[(dr, pt)] = [chi2_x, chi2_p]

    return fisher_exact_dict, chi2_or_fisher_exact_dict

def combined_ppmi_and_statistical_association(statistical_association_df_list, ppmi_df_list):

    significant_pairs = {}

    for i in range(len(statistical_association_df_list)):

        for _, row in statistical_association_df_list[i].iterrows():
            pt, dr, p_value = row["PT"], row["DR"], row["P-Value"]

            if (ppmi_df_list[i].loc[dr, pt] >= 1) and (p_value < 0.05):
                if (pt, dr) not in significant_pairs:
                    significant_pairs[(pt, dr)] = {}
                significant_pairs[(pt, dr)][i] = 'X'

    all_pairs = [(pt, dr) for pt, dr in significant_pairs.keys()]

    #used chatgpt for this
    all_indices = sorted({idx for pair_dict in significant_pairs.values() for idx in pair_dict})

    result_df = pd.DataFrame(index=all_pairs, columns=all_indices, data="")

    result_df.index = pd.MultiIndex.from_tuples(result_df.index, names=["PT", "DR"])

    for (pt, dr), idx_dict in significant_pairs.items():
        for idx in idx_dict:
            result_df.loc[(pt, dr), idx] = 'X'

    print(result_df)

    return result_df

def dict_to_df(fisher_exact_dict, chi2_or_fisher_exact_dict):

    fisher_p_df = pd.DataFrame(
        [(pt, dr, p) for (dr, pt), (_, p) in fisher_exact_dict.items()],
        columns=["PT", "DR", "P-Value"]
    )
    fisher_x_df = pd.DataFrame(
        [(pt, dr, x) for (dr, pt), (x, _) in fisher_exact_dict.items()],
        columns=["PT", "DR", "X-Value"]
    )

    combined_p_df = pd.DataFrame(
        [(pt, dr, p) for (dr, pt), (_, p) in chi2_or_fisher_exact_dict.items()],
        columns=["PT", "DR", "P-Value"]
    )
    combined_x_df = pd.DataFrame(
        [(pt, dr, x) for (dr, pt), (x, _) in chi2_or_fisher_exact_dict.items()],
        columns=["PT", "DR", "X-Value"]
    )

    return fisher_p_df, fisher_x_df, combined_p_df, combined_x_df

