import matplotlib.pyplot as plt
import seaborn as sns

def calculate_probabilities(dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict, total_count):

    dr_prob = {}
    pt_prob = {}
    joint_prob = {}

    for dr, count in dr_freq_dict.items():
        dr_prob[dr] = count / total_count

    for pt, count in pt_freq_dict.items():
        pt_prob[pt] = count / total_count

    for (dr, pt), count in cooccurrence_freq_dict.items():
        joint_prob[(dr, pt)] = count / total_count

    return dr_prob, pt_prob, joint_prob

def naive_bayes(dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict):

    nb_prob = {}
    for (dr, pt), count in cooccurrence_freq_dict.items():
        nb_prob[(dr, pt)] = count / pt_freq_dict[pt]
    return nb_prob

def compute_pt_given_dr(joint_prob, dr_prob):

    pt_given_dr = {}

    for (dr, pt), joint_p in joint_prob.items():
        pt_given_dr[(dr, pt)] = joint_p / dr_prob[dr]

    return pt_given_dr

def find_top_drs_by_pt_given_dr(pt_freq_dict, joint_prob, dr_prob, top_pt_count=4, top_dr_count=3):
    """
    Find the top DRs for the top PTs based on P(PT | DR).

    Parameters:
    - pt_freq_dict: Dictionary with PT frequencies.
    - joint_prob: Dictionary with joint probabilities P(DR, PT).
    - dr_prob: Dictionary with DR probabilities P(DR).
    - top_pt_count: Number of top PTs to consider.
    - top_dr_count: Number of top DRs for each PT.

    Returns:
    - result: Dictionary where keys are PTs and values are lists of top DRs based on P(PT|DR).
    """
    # Step 1: Get the top N most occurring PTs
    top_pts = sorted(pt_freq_dict.items(), key=lambda x: x[1], reverse=True)[:top_pt_count]

    result = {}

    # Step 2: For each top PT, calculate P(PT | DR) and find the top DRs
    for pt, _ in top_pts:
        pt_given_dr = {}

        # Compute P(PT | DR) for the current PT
        for (dr, pt_), joint_p in joint_prob.items():
            if pt_ == pt:  # Only include this PT
                pt_given_dr[dr] = joint_p / dr_prob[dr]

        # Sort DRs by P(PT | DR) and select the top N
        top_drs = sorted(pt_given_dr.items(), key=lambda x: x[1], reverse=True)[:top_dr_count]

        # Add to result
        result[pt] = top_drs

    return result

#used chatgpt for formatting
def plot_cooccurrence_bar_chart(cooccurrence_freq_dict, output_path="cooccurrence_bar_chart.png"):
    # Convert co-occurrence dictionary to a DataFrame for easier plotting
    cooccurrence_df = pd.DataFrame([
        {"DR": dr, "PT": pt, "Frequency": freq}
        for (dr, pt), freq in cooccurrence_freq_dict.items()
    ])

    # Sort by frequency for better visualization
    cooccurrence_df = cooccurrence_df.sort_values(by="Frequency", ascending=False)

    # Combine DR and PT into a single label
    cooccurrence_df["DR_PT"] = cooccurrence_df["DR"] + " | " + cooccurrence_df["PT"]

    # Create a bar chart
    plt.figure(figsize=(15, len(cooccurrence_df) * 0.3))  # Adjust figure height dynamically
    sns.barplot(
        data=cooccurrence_df,
        x="Frequency",
        y="DR_PT",
        palette="Blues_d"
    )
    plt.title("Frequency of Co-Occurrence (DR | PT)", fontsize=16)
    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("DR | PT Pair", fontsize=12)

    # Adjust y-axis tick labels
    plt.gca().yaxis.set_tick_params(labelsize=10)  # Set font size for labels
    plt.gca().tick_params(axis='y', which='major', pad=10)  # Add padding to y-axis labels

    # Use tight layout to prevent label clipping
    plt.tight_layout()

    # Save the figure as an image
    plt.savefig(output_path, dpi=300, bbox_inches="tight")  # High DPI for clarity

    # Show the chart
    plt.show()