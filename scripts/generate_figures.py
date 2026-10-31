"""Regenerate the SVG charts in the README from the original observations."""
from collections import defaultdict
from pathlib import Path
from html import escape
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
FIELDS = {"precip": 1, "tmax": 3, "tmin": 4}


def monthly_statistics():
    groups = defaultdict(lambda: defaultdict(list))
    for line in (ROOT / "ClimatologiaNavojoa.txt").read_text(encoding="utf-8-sig").splitlines():
        parts = line.split()
        if len(parts) != 5 or not re.fullmatch(r"\d{2}/\d{2}/\d{4}", parts[0]):
            continue
        month = int(parts[0][3:5])
        for label, col in FIELDS.items():
            if parts[col] != "Nulo":
                groups[month][label].append(float(parts[col]))
    result = []
    for m in range(1, 13):
        record = {"month": m}
        for label in FIELDS:
            values = groups[m][label]
            record[label] = sum(values) / len(values) if values else None
            record["n_" + label] = len(values)
        result.append(record)
    return result


def base(title, subtitle):
    return ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="440" viewBox="0 0 960 440">',
            '<rect width="960" height="440" fill="#ffffff"/>',
            f'<text x="62" y="48" font-family="Arial" font-size="25" font-weight="700" fill="#172b4d">{escape(title)}</text>',
            f'<text x="62" y="74" font-family="Arial" font-size="13" fill="#52677d">{escape(subtitle)}</text>',
            '<line x1="82" y1="350" x2="913" y2="350" stroke="#718096"/>']


def precipitation_chart(data):
    parts = base("Seasonal precipitation in Navojoa", "Mean daily precipitation by calendar month | Station 26131 | 1931–1993")
    for tick in range(5):
        y = 350 - tick * 66
        parts += [f'<line x1="82" y1="{y}" x2="913" y2="{y}" stroke="#e7edf3"/>',
                  f'<text x="69" y="{y+5}" text-anchor="end" font-family="Arial" font-size="12">{tick}</text>']
    for i, row in enumerate(data):
        x = 104 + 68.1 * i
        if row["precip"] is not None:
            y = 350 - row["precip"] * 66
            parts.append(f'<rect x="{x-18:.2f}" y="{y:.2f}" width="36" height="{350-y:.2f}" fill="#2878a6" rx="3"/>')
        parts.append(f'<text x="{x:.2f}" y="374" text-anchor="middle" font-family="Arial" font-size="12">{MONTHS[i]}</text>')
    parts += ['<text x="17" y="233" transform="rotate(-90 17 233)" text-anchor="middle" font-family="Arial" font-size="12">Mean daily precipitation (mm)</text>',
              '<text x="82" y="414" font-family="Arial" font-size="12">Missing values excluded; not monthly precipitation totals.</text>', '</svg>']
    return "\n".join(parts) + "\n"


def temperature_chart(data):
    parts = base("Seasonal temperatures in Navojoa", "Recorded daily maximum and minimum, grouped by month | Station 26131")
    def ypos(value):
        return 350 - value / 45 * 236
    for tick in range(0, 41, 10):
        y = ypos(tick)
        parts += [f'<line x1="82" y1="{y:.2f}" x2="913" y2="{y:.2f}" stroke="#e7edf3"/>',
                  f'<text x="69" y="{y+5:.2f}" text-anchor="end" font-family="Arial" font-size="12">{tick}</text>']
    for label, color in (("tmax", "#d4653a"), ("tmin", "#257da8")):
        pts = " ".join(f'{104+68.1*i:.1f},{ypos(row[label]):.1f}' for i, row in enumerate(data) if row[label] is not None)
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3"/>')
        for i, row in enumerate(data):
            if row[label] is not None:
                parts.append(f'<circle cx="{104+68.1*i:.1f}" cy="{ypos(row[label]):.1f}" r="4" fill="{color}"/>')
    for i, month in enumerate(MONTHS):
        parts.append(f'<text x="{104+68.1*i:.2f}" y="374" text-anchor="middle" font-family="Arial" font-size="12">{month}</text>')
    parts += ['<text x="17" y="233" transform="rotate(-90 17 233)" text-anchor="middle" font-family="Arial" font-size="12">Temperature (°C)</text>',
              '<text x="340" y="404" font-family="Arial" fill="#d4653a">● Mean Tmax</text>',
              '<text x="530" y="404" font-family="Arial" fill="#257da8">● Mean Tmin</text>', '</svg>']
    return "\n".join(parts) + "\n"


def main():
    data = monthly_statistics()
    figures = ROOT / "reports" / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    (figures / "monthly_precipitation.svg").write_text(precipitation_chart(data), encoding="utf-8")
    (figures / "monthly_temperatures.svg").write_text(temperature_chart(data), encoding="utf-8")
    with (ROOT / "reports" / "monthly_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["month", "mean_daily_precipitation_mm", "n_precip", "mean_daily_tmax_c", "n_tmax", "mean_daily_tmin_c", "n_tmin"])
        for row in data:
            writer.writerow([row["month"], *[value for key in FIELDS for value in (round(row[key], 4) if row[key] is not None else "", row["n_" + key])]])
    print("Regenerated CSV and README figures")


if __name__ == "__main__":
    main()
