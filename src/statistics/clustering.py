from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

##chatgpt used for formatting
def cluster_and_plot_3d(filtered_ppmi, n_clusters):

    filtered_ppmi = filtered_ppmi.loc[:, (filtered_ppmi != 0).any(axis=0)]

    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(filtered_ppmi)
    labels = kmeans.labels_

    pca = PCA(n_components=3)
    components = pca.fit_transform(filtered_ppmi)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(components[:, 0], components[:, 1], components[:, 2], c=labels, cmap='viridis', s=100)

    for i, pt in enumerate(filtered_ppmi.index):
        ax.text(components[i, 0], components[i, 1], components[i, 2], pt)

    ax.set_title("3D Clustering of PTs based on PPMI Vectors")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")

    plt.show()
