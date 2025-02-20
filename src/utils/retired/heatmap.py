import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
#used chatgpt to format
def plot_pt_dr_ppmi_heatmap(ppmi, i):
    print(ppmi)

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

    plt.savefig(output_path, dpi=300, bbox_inches="tight")


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

    plt.savefig(output_path, dpi=300, bbox_inches="tight")

#used chatgpt to format
def plot_significant_pairs_heatmap(result_df):

    numerical_df = result_df.replace("X", 1).fillna(0).astype(int)

    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(
        numerical_df,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False
    )

    ax.set_title("Significant Pairs", fontsize=16)
    ax.set_xlabel("Indices (i)", fontsize=12)
    ax.set_ylabel("PT, DR Pairs", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10, rotation=0)

    plt.tight_layout()

    output_path = f"Significant_Pairs_Heatmap.png"

    plt.savefig(output_path, dpi=300, bbox_inches="tight")


