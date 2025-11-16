
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_samples, silhouette_score
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.cm as cm

DATA_PATH = Path("/Users/ooooona/Downloads/477/mendeley_clean.csv")
FIG_DIR = Path("report_outputs/figs")
TAB_DIR = Path("report_outputs/tables")

sns.set(style="whitegrid")


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[load_data] Loaded {path}, shape = {df.shape}")
    return df


def prepare_features(df: pd.DataFrame):

    numeric = df.select_dtypes(include=[np.number]).copy()

    gender = None
    if "Gender" in numeric.columns:
        gender = numeric["Gender"].copy()
        numeric = numeric.drop(columns=["Gender"])

    if "index" in numeric.columns:
        numeric = numeric.drop(columns=["index"])

    print(f"[prepare_features] Feature columns: {list(numeric.columns)}")

    scaler = StandardScaler()
    X_scaled_np = scaler.fit_transform(numeric)
    X_scaled = pd.DataFrame(X_scaled_np, columns=numeric.columns)

    return numeric, X_scaled, gender


def run_kmeans(X_scaled: pd.DataFrame,
               n_clusters: int = 8,
               random_state: int = 100):
    """Fit k-means and return model + labels."""
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init="auto"
    )
    labels = kmeans.fit_predict(X_scaled)
    print(f"[run_kmeans] k = {n_clusters}, inertia = {kmeans.inertia_:.2f}")
    return kmeans, labels


def run_hac(X_scaled: pd.DataFrame,
            n_clusters: int = 3,
            linkage_method: str = "ward"):
    hac = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage_method
    )
    labels = hac.fit_predict(X_scaled)
    print(f"[run_hac] k = {n_clusters}, linkage = {linkage_method}")
    return hac, labels


def silhouette_plot(X_scaled: pd.DataFrame,
                    labels: np.ndarray,
                    name: str):
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    n_clusters = len(np.unique(labels))
    silhouette_avg = silhouette_score(X_scaled, labels)
    sample_silhouette_values = silhouette_samples(X_scaled, labels)

    print(f"[silhouette_plot] {name}: average silhouette = {silhouette_avg:.3f}")

    fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
    ax1.set_xlim([-0.1, 1])
    ax1.set_ylim([0, len(X_scaled) + (n_clusters + 1) * 10])

    y_lower = 10
    for i in range(n_clusters):
        ith_cluster_silhouette_values = sample_silhouette_values[labels == i]
        ith_cluster_silhouette_values.sort()
        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7,
        )

        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        y_lower = y_upper + 10

    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    ax1.set_title(f"Silhouette plot ({name})")
    ax1.set_xlabel("Silhouette coefficient")
    ax1.set_ylabel("Cluster label")
    ax1.set_yticks([])
    ax1.set_xticks(np.linspace(-0.1, 1.0, 7))

    fig.tight_layout()
    out_path = FIG_DIR / f"silhouette_{name}.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    return silhouette_avg


def tsne_plots(X_scaled: pd.DataFrame,
               kmeans_labels: np.ndarray,
               hac_labels: np.ndarray):
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    tsne = TSNE(n_components=2, perplexity=40, random_state=90)
    embedding = tsne.fit_transform(X_scaled)
    df_tsne = pd.DataFrame(embedding, columns=["x_proj", "y_proj"])
    df_tsne["kmeans_label"] = kmeans_labels
    df_tsne["hac_label"] = hac_labels

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sns.scatterplot(
        data=df_tsne,
        x="x_proj", y="y_proj",
        hue="kmeans_label",
        palette=sns.color_palette("husl", len(np.unique(kmeans_labels))),
        ax=axes[0]
    )
    axes[0].set_title("t-SNE with k-means labels (k=8)")
    axes[0].legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    sns.scatterplot(
        data=df_tsne,
        x="x_proj", y="y_proj",
        hue="hac_label",
        palette=sns.color_palette("husl", len(np.unique(hac_labels))),
        ax=axes[1]
    )
    axes[1].set_title("t-SNE with HAC labels (k=3, ward)")
    axes[1].legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    fig.tight_layout()
    out_path = FIG_DIR / "tsne_kmeans_hac.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def boxplots_by_cluster(df_scaled: pd.DataFrame):
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    for col in df_scaled.columns:
        if col in ["Gender", "predicted_cluster"]:
            continue
        plt.figure(figsize=(6, 4))
        sns.boxplot(
            x="predicted_cluster",
            y=col,
            data=df_scaled
        )
        plt.title(f"{col} by k-means cluster")
        out_path = FIG_DIR / f"boxplot_{col}.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()


def ward_dendrogram(X_scaled: pd.DataFrame):
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    linkage_matrix = linkage(X_scaled, method="ward")

    plt.figure(figsize=(12, 8))
    dendrogram(
        linkage_matrix,
        truncate_mode="lastp",
        p=25,
        leaf_rotation=45,
        leaf_font_size=10,
        show_contracted=True
    )
    plt.title("Hierarchical Clustering Dendrogram (ward linkage)")
    plt.xlabel("Cluster index / size")
    plt.ylabel("Distance")
    plt.axhline(y=30, color="red", linestyle="--")
    plt.tight_layout()
    out_path = FIG_DIR / "dendrogram_ward.png"
    plt.savefig(out_path, dpi=300)
    plt.close()


def save_cluster_sizes(kmeans_labels, hac_labels):
    TAB_DIR.mkdir(parents=True, exist_ok=True)

    k_series = pd.Series(kmeans_labels, name="kmeans_cluster")
    h_series = pd.Series(hac_labels, name="hac_cluster")

    k_counts = k_series.value_counts().sort_index()
    h_counts = h_series.value_counts().sort_index()

    k_df = k_counts.reset_index()
    k_df.columns = ["cluster", "count"]
    k_df.to_csv(TAB_DIR / "kmeans_cluster_counts.csv", index=False)

    h_df = h_counts.reset_index()
    h_df.columns = ["cluster", "count"]
    h_df.to_csv(TAB_DIR / "hac_cluster_counts.csv", index=False)

    print("[save_cluster_sizes] Saved cluster size tables.")


def main():
    df = load_data()

    X, X_scaled, gender = prepare_features(df)

    kmeans, kmeans_labels = run_kmeans(X_scaled, n_clusters=8, random_state=100)

    hac, hac_labels = run_hac(X_scaled, n_clusters=3, linkage_method="ward")

    silhouette_plot(X_scaled, kmeans_labels, name="kmeans_k8")

    tsne_plots(X_scaled, kmeans_labels, hac_labels)

    df_scaled = X_scaled.copy()
    if gender is not None:
        df_scaled["Gender"] = gender.values
    df_scaled["predicted_cluster"] = kmeans_labels
    boxplots_by_cluster(df_scaled)

    ward_dendrogram(X_scaled)

    TAB_DIR.mkdir(parents=True, exist_ok=True)
    df_with_clusters = df.copy()
    df_with_clusters["kmeans_cluster"] = kmeans_labels
    df_with_clusters["hac_cluster"] = hac_labels
    df_with_clusters.to_csv(
        TAB_DIR / "mendeley_with_clusters.csv",
        index=False
    )
    save_cluster_sizes(kmeans_labels, hac_labels)

    print("[main] Done. Figures -> ./report_outputs/figs ; Tables -> ./report_outputs/tables")


if __name__ == "__main__":
    main()
