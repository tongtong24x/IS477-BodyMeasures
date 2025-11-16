

import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR = Path("/Users/ooooona/Downloads/477")
DATA_PATH = BASE_DIR / "integrated_anthro.csv"
FIG_DIR = BASE_DIR / "report_outputs" / "figs"

sns.set(style="whitegrid")


def main():
    df = pd.read_csv(DATA_PATH)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 4))
    sns.histplot(data=df, x="Age", hue="source", kde=True, stat="density", common_norm=False)
    plt.title("Age distribution by source")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "integrated_age_by_source.png", dpi=300)
    plt.close()

    plt.figure(figsize=(5, 4))
    sns.boxplot(data=df, x="source", y="TotalHeight")
    plt.title("TotalHeight by source")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "integrated_height_by_source.png", dpi=300)
    plt.close()

    plt.figure(figsize=(5, 4))
    sns.boxplot(data=df, x="source", y="Waist")
    plt.title("Waist by source")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "integrated_waist_by_source.png", dpi=300)
    plt.close()

    print("[integrated_analysis] Saved plots to:", FIG_DIR)


if __name__ == "__main__":
    main()