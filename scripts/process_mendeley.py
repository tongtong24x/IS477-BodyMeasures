#process_mendeley.py

import pandas as pd
from pathlib import Path

RAW_PATH = Path("/Users/ooooona/Downloads/477/BodyMeasurements _ original_CSV.csv")
OUT_PATH = Path("/Users/ooooona/Downloads/477/mendeley_clean.csv")


def load_raw() -> pd.DataFrame:
    df = pd.read_csv(RAW_PATH)
    return df


def clean_mendeley(df: pd.DataFrame) -> pd.DataFrame:

    df = df.dropna().reset_index(drop=False)

    rename_map = {
        "Height": "height_cm",
        "Weight": "weight_kg",
        "BMI": "BMI",
        "Waist": "waist_cm",
        "Chest": "chest_cm",
    }
    for old, new in rename_map.items():
        if old in df.columns:
            df = df.rename(columns={old: new})

    return df


def main():
    print(f"Loading raw Mendeley data from: {RAW_PATH}")
    df_raw = load_raw()
    print(f"Raw shape: {df_raw.shape}")

    df_clean = clean_mendeley(df_raw)
    print(f"Cleaned shape: {df_clean.shape}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUT_PATH, index=False)
    print(f"Saved cleaned data to: {OUT_PATH}")


if __name__ == "__main__":
    main()
