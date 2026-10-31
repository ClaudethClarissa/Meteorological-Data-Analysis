"""Shared, reproducible data cleaning for Navojoa station observations."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "ClimatologiaNavojoa.txt"

def load_daily():
    df = pd.read_csv(DATA, skiprows=19, sep=r"\s+", names=["date","precip_mm","evap_mm","tmax_c","tmin_c"], dtype=str)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date"]).copy()
    for column in ["precip_mm","evap_mm","tmax_c","tmin_c"]:
        df[column] = pd.to_numeric(df[column].replace("Nulo",pd.NA), errors="coerce")
    df = df.drop(columns=["evap_mm"]).sort_values("date").reset_index(drop=True)
    df["year"] = df.date.dt.year
    df["month"] = df.date.dt.month
    return df

def monthly_climatology(df):
    return df.groupby("month").agg(
        mean_daily_precip_mm=("precip_mm","mean"),
        precipitation_observations=("precip_mm","count"),
        mean_tmax_c=("tmax_c","mean"),
        mean_tmin_c=("tmin_c","mean"),
    ).reset_index()

def annual_summary(df):
    # An annual total requires coverage checks before comparison.
    return df.groupby("year").agg(
        observed_precip_total_mm=("precip_mm","sum"),
        precipitation_observations=("precip_mm","count"),
        mean_tmax_c=("tmax_c","mean"),
        mean_tmin_c=("tmin_c","mean"),
    ).reset_index()
