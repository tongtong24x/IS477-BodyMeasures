
import pandas as pd
from pathlib import Path

BMX_PATH = Path("/Users/ooooona/Downloads/477/BMX_L.xpt")
DEMO_PATH = Path("/Users/ooooona/Downloads/477/DEMO_L.xpt")

OUT_PATH = Path("/Users/ooooona/Downloads/477/nhanes_clean.csv")


def main():

    print("[process_nhanes] Loading NHANES XPT files...")

    bmx = pd.read_sas(BMX_PATH, format="xport")
    demo = pd.read_sas(DEMO_PATH, format="xport")

    print(f"BMX shape: {bmx.shape}")
    print(f"DEMO shape: {demo.shape}")

    demo_small = demo[["SEQN", "RIDAGEYR", "RIAGENDR"]]

    df = bmx.merge(demo_small, on="SEQN", how="inner")
    print(f"Merged shape: {df.shape}")

    df = df[df["RIDAGEYR"] >= 18]

    df = df.rename(columns={
        "RIDAGEYR": "Age",
        "RIAGENDR": "Gender",
        "BMXWAIST": "Waist",
        "BMXHT": "TotalHeight"
    })

    keep_cols = ["SEQN", "Gender", "Age", "Waist", "TotalHeight"]
    df = df[keep_cols]

    df = df.dropna()

    print(f"Final cleaned NHANES shape: {df.shape}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"[process_nhanes] Saved cleaned dataset → {OUT_PATH}")


if __name__ == "__main__":
    main()
