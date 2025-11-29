# scripts/extract/ingest_gdelt_local.py

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

# Repo root (scripts/extract/ -> scripts -> root)
BASE_DIR = Path(__file__).resolve().parents[2]


def load_raw_gdelt():
    raw_path = BASE_DIR / "data" / "raw" / "gdelt" / "sample_events.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw GDELT file not found at {raw_path}")

    print(f"[+] Loading raw GDELT file: {raw_path}")
    df = pd.read_csv(raw_path, encoding="latin1", engine="python", sep="\t", header=None, on_bad_lines="skip")
    gdelt_columns = [
        "GLOBALEVENTID",
        "SQLDATE",
        "MonthYear",
        "Year",
        "FractionDate",
        "Actor1Code",
        "Actor1Name",
        "Actor1CountryCode",
        "Actor1KnownGroupCode",
        "Actor1EthnicCode",
        "Actor1Religion1Code",
        "Actor1Religion2Code",
        "Actor1Type1Code",
        "Actor1Type2Code",
        "Actor1Type3Code",
        "Actor2Code",
        "Actor2Name",
        "Actor2CountryCode",
        "Actor2KnownGroupCode",
        "Actor2EthnicCode",
        "Actor2Religion1Code",
        "Actor2Religion2Code",
        "Actor2Type1Code",
        "Actor2Type2Code",
        "Actor2Type3Code",
        "IsRootEvent",
        "EventCode",
        "EventBaseCode",
        "EventRootCode",
        "QuadClass",
        "GoldsteinScale",
        "NumMentions",
        "NumSources",
        "NumArticles",
        "AvgTone",
        "Actor1Geo_Type",
        "Actor1Geo_FullName",
        "Actor1Geo_CountryCode",
        "Actor1Geo_ADM1Code",
        "Actor1Geo_ADM2Code",
        "Actor1Geo_Lat",
        "Actor1Geo_Long",
        "Actor1Geo_FeatureID",
        "Actor2Geo_Type",
        "Actor2Geo_FullName",
        "Actor2Geo_CountryCode",
        "Actor2Geo_ADM1Code",
        "Actor2Geo_ADM2Code",
        "Actor2Geo_Lat",
        "Actor2Geo_Long",
        "Actor2Geo_FeatureID",
        "ActionGeo_Type",
        "ActionGeo_FullName",
        "ActionGeo_CountryCode",
        "ActionGeo_ADM1Code",
        "ActionGeo_ADM2Code",
        "ActionGeo_Lat",
        "ActionGeo_Long",
        "ActionGeo_FeatureID",
        "DATEADDED",
        "SOURCEURL"
    ]

    df.columns = gdelt_columns
    print(f"[+] Loaded {len(df):,} rows, {len(df.columns)} columns")
    return df


def normalize_gdelt(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes GDELT Events table to a SOC-friendly schema.
    """

    column_map = {
        "GLOBALEVENTID": "event_id",
        "SQLDATE": "event_date",
        "Actor1Name": "actor1_name",
        "Actor1CountryCode": "actor1_country",
        "Actor2Name": "actor2_name",
        "Actor2CountryCode": "actor2_country",
        "ActionGeo_CountryCode": "geo_country",
        "ActionGeo_Lat": "geo_lat",
        "ActionGeo_Long": "geo_long",
        "EventCode": "event_code",
        "GoldsteinScale": "impact_score",
        "NumMentions": "num_mentions",
        "NumSources": "num_sources",
        "NumArticles": "num_articles",
        "AvgTone": "avg_tone",
    }

    available = {k: v for k, v in column_map.items() if k in df.columns}
    missing = [k for k in column_map if k not in df.columns]

    if missing:
        print(f"[!] Missing expected columns (skipped): {missing}")

    df_small = df[list(available.keys())].rename(columns=available)

    # Convert date
    if "event_date" in df_small.columns:
        df_small["event_date"] = pd.to_datetime(
            df_small["event_date"], format="%Y%m%d", errors="coerce"
        )

    # Convert numbers
    numeric_cols = ["impact_score", "num_mentions", "num_sources", "num_articles", "avg_tone"]

    for col in numeric_cols:
        if col in df_small.columns:
            df_small[col] = pd.to_numeric(df_small[col], errors="coerce")

    # Drop invalid rows
    for key in ["event_id", "event_date"]:
        if key in df_small.columns:
            df_small = df_small[df_small[key].notna()]

    print(f"[+] Normalized -> {len(df_small):,} rows, {len(df_small.columns)} columns")
    return df_small


def save_processed(df: pd.DataFrame):
    out_dir = BASE_DIR / "data" / "processed" / "gdelt"
    out_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = out_dir / "gdelt_events.parquet"
    csv_path = out_dir / "gdelt_events.csv"

    print(f"[+] Saving Parquet -> {parquet_path}")
    df.to_parquet(parquet_path, index=False)

    print(f"[+] Saving CSV -> {csv_path}")
    df.to_csv(csv_path, index=False)

    print("[+] Done saving.")


def main():
    load_dotenv(BASE_DIR / ".env", override=True)

    df_raw = load_raw_gdelt()
    df_norm = normalize_gdelt(df_raw)
    save_processed(df_norm)


if __name__ == "__main__":
    main()
