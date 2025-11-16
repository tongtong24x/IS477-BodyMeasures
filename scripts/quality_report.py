
import pandas as pd
from pathlib import Path

PROC_DIR = Path("/Users/ooooona/Downloads/477")
OUT_DIR = Path("report_outputs/tables")


def summarize(df: pd.DataFrame, name: str):
    cols = [c for c in ["Age", "Waist", "TotalHeight"] if c in df.columns]
    summary = df[cols].describe()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{name}_summary.csv"
    summary.to_csv(out_path)
    print(f"[quality_report] Saved summary for {name} -> {out_path}")


def main():
    m = pd.read_csv(PROC_DIR / "mendeley_clean.csv")
    n = pd.read_csv(PROC_DIR / "nhanes_clean.csv")
    integ = pd.read_csv(PROC_DIR / "integrated_anthro.csv")

    summarize(m, "mendeley")
    summarize(n, "nhanes")
    summarize(integ, "integrated")


if __name__ == "__main__":
    main()
