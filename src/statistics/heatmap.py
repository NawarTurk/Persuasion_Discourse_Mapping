import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#used chatgpt to format
def plot_pt_dr_ppmi_heatmap(ppmi, i):

    plt.figure(figsize=(12, 8))
    sns.heatmap(ppmi, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'PPMI'})
    plt.title("Filtered Heatmap of PPMI Values", fontsize=16)
    plt.xlabel("Persuasion Techniques (PT)", fontsize=12)
    plt.ylabel("Discourse Relations (DR)", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    # plt.show()

    output_path = f"Filtered_HeatMap_Of_PT_DR_PPMI_Values_Pooling_{i}.png"

    plt.savefig(output_path, dpi=300, bbox_inches="tight")  # High DPI for clarity


#used chatgpt to format
def plot_pt_pt_cosine_similarity_heatmap(cosine_sim_matrix, i):

    plt.figure(figsize=(12, 8))
    sns.heatmap(cosine_sim_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Cosine Similarity'})
    plt.title("Filtered Heatmap of PT-PT Cosine Similarity", fontsize=16)
    plt.xlabel("Persuasion Techniques (PT)", fontsize=12)
    plt.ylabel("Persuasion Techniques (PT)", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    # plt.show()

    output_path = f"Filtered_HeatMap_Of_PT_PT_PPMI_Values_Pooling_{i}.png"

    plt.savefig(output_path, dpi=300, bbox_inches="tight")  # High DPI for clarity


