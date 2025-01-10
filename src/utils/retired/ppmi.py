import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def calculate_ppmi(dr_prob, pt_prob, joint_prob):

    ppmi = {}
    for (dr, pt), p_joint in joint_prob.items():
        pmi = np.log2(p_joint / (pt_prob[pt] * dr_prob[dr]))
        ppmi[(dr, pt)] = max(pmi, 0)
    return ppmi

def create_ppmi_df(ppmi, dr_list, pt_list):

    ppmi_df = pd.DataFrame(0.0, index=dr_list, columns=pt_list)

    for (dr, pt), value in ppmi.items():
        ppmi_df.loc[dr, pt] = value

    return ppmi_df


def create_filtered_ppmi_df(ppmi, pt_freq_dict, dr_freq_dict, pt_filter_nb, dr_filter_nb):
    filtered_pts = []
    for pt, freq in pt_freq_dict.items():
        if freq > pt_filter_nb:
            print(freq)
            filtered_pts.append(pt)

    filtered_drs = []
    for dr, freq in dr_freq_dict.items():
        if freq > dr_filter_nb:
            print(freq)

            filtered_drs.append(dr)

    ppmi_filtered_df = pd.DataFrame(0.0, index=filtered_drs, columns=filtered_pts)

    for (dr, pt), value in ppmi.items():
        if dr in filtered_drs and pt in filtered_pts:
            ppmi_filtered_df.loc[dr, pt] = value

    return ppmi_filtered_df

def compute_cosine_similarity(ppmi_vectors):
    # print(ppmi_vectors)

    similarity_matrix = cosine_similarity(ppmi_vectors)
    # print(similarity_matrix)
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=ppmi_vectors.index,
        columns=ppmi_vectors.index
    )
    return similarity_df
