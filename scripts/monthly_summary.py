"""Summarize climatological observations by calendar month using the standard library.

Run from the repository root: python scripts/monthly_summary.py
Produces a CSV of mean observed daily precipitation and temperatures with nonmissing counts.
"""
from collections import defaultdict
from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ClimatologiaNavojoa.txt"
OUTPUT = ROOT / "reports" / "monthly_summary.csv"
DATE_PATTERN = re.compile(r"^\d{2}/\d{2}/\d{4}$")
COLUMNS = {"precipitation_mm": 1, "tmax_c": 3, "tmin_c": 4}


def main():
    measurements = defaultdict(lambda: defaultdict(list))
    with SOURCE.open(encoding="utf-8-sig") as infile:
        for line in infile:
            values = line.split()
            if len(values) != 5 or not DATE_PATTERN.fullmatch(values[0]):
                continue
            month = int(values[0][3:5])
            for name, index in COLUMNS.items():
                if values[index] != "Nulo":
                    measurements[month][name].append(float(values[index]))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["month", "mean_daily_precipitation_mm", "n_precip",
                         "mean_daily_tmax_c", "n_tmax",
                         "mean_daily_tmin_c", "n_tmin"])
        for month in range(1, 13):
            vals = measurements[month]
            writer.writerow([month, *(
                entry
                for name in COLUMNS
                for entry in (
                    round(sum(vals[name]) / len(vals[name]), 4) if vals[name] else "",
                    len(vals[name]),
                )
            )])
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
