import pandas as pd
from pathlib import Path

PROC_DIR = Path("/Users/ooooona/Downloads/477")
OUT_PATH = PROC_DIR / "integrated_anthro.csv"


def main():
    m_path = PROC_DIR / "mendeley_clean.csv"
    n_path = PROC_DIR / "nhanes_clean.csv"

    print(f"[integrate] Loading: {m_path}")
    m = pd.read_csv(m_path)

    print(f"[integrate] Loading: {n_path}")
    n = pd.read_csv(n_path)

    m.columns = m.columns.str.strip()
    n.columns = n.columns.str.strip()

    print("[integrate] Mendeley columns:", list(m.columns))
    print("[integrate] NHANES columns:", list(n.columns))

    m_sub = m[["Gender", "Age", "Waist", "TotalHeight"]].copy()
    n_sub = n[["Gender", "Age", "Waist", "TotalHeight"]].copy()

    m_sub["source"] = "Mendeley"
    n_sub["source"] = "NHANES"

    integrated = pd.concat([m_sub, n_sub], ignore_index=True)

    print("[integrate] Integrated shape:", integrated.shape)
    print(integrated["source"].value_counts())

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    integrated.to_csv(OUT_PATH, index=False)
    print(f"[integrate] Saved integrated dataset -> {OUT_PATH}")


if __name__ == "__main__":
    main()
