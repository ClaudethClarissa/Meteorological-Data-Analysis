# Historical Climate Analysis | Navojoa, Mexico 🌦️

**Exploratory Data Analysis · Data Cleaning · Time Series Visualization**

A Python-based exploration of historical daily weather observations from **Navojoa (FFCC) station 26131**, Sonora, Mexico. The project studies the seasonal distribution of precipitation and maximum/minimum temperatures, and illustrates how rolling averages reveal patterns at different time scales.

[**Exploratory Data Analysis**](BD_Climatologica_Navojoa.ipynb) · [**Time Series Analysis**](Climatologia_Navojoa_Series_Tiempo.ipynb) · [**Return to my portfolio**](https://github.com/ClaudethClarissa/data-science-portfolio)

---

## Project at a glance

| | |
|---|---|
| **Location** | Navojoa, Sonora, Mexico |
| **Station** | Navojoa (FFCC), ID 26131 |
| **Coordinates** | 27.081° N, 109.445° W |
| **Elevation** | 41 m above sea level |
| **Available daily record** | January 1931 – July 1993 (with missing observations and unequal coverage) |
| **Variables analyzed** | Daily precipitation (mm), maximum and minimum air temperature (°C) |
| **Tools** | Python, pandas, NumPy, Matplotlib, Seaborn, statsmodels, Jupyter Notebook |

## Questions explored

- How are precipitation and temperature distributed across the calendar year?
- How do observed temperatures and precipitation vary across years?
- What becomes visible when daily temperatures are smoothed with moving averages at different time scales?
- What limitations must be considered when interpreting an incomplete historical record?

## Data source

The daily observations in [`ClimatologiaNavojoa.txt`](ClimatologiaNavojoa.txt) are labeled **CNA–SMN** (Mexico's National Meteorological Service), with a file issue date of April 6, 2020. The file identifies station 26131 as **Navojoa (FFCC)** and notes the station's status as suspended.

Two additional reference files are provided:
- [`ExtremosNavojoa.TXT`](ExtremosNavojoa.TXT): monthly historical extremes and related statistics.
- [`NORMAL26131.TXT`](NORMAL26131.TXT): published climatological normals, labeled **1951–2010**. These reference values should not be treated as estimates from the entire 1931–1993 daily record.

The original file includes an evaporation column, but the analysis omits it because the supplied daily observations do not contain usable evaporation values.

## Analyses

The two Jupyter notebooks contain the code, explanations, and visual results for this project:

- [Exploratory Data Analysis](BD_Climatologica_Navojoa.ipynb): data preparation, monthly and annual summaries, histograms, density estimates (KDE), and boxplots.
- [Time Series Analysis](Climatologia_Navojoa_Series_Tiempo.ipynb): historical precipitation and temperature records, selected time periods, and moving averages.

Both notebooks include executed charts and tables for direct viewing on GitHub. Supporting data, scripts, and tests are included for reproducibility.

## Analysis workflow

### 1. Data preparation & exploratory analysis

[`BD_Climatologica_Navojoa.ipynb`](BD_Climatologica_Navojoa.ipynb)

- Load the station's text-formatted daily observations.
- Replace the source's `Nulo` entries with missing values.
- Convert temperature and precipitation to numeric data and parse dates.
- Derive calendar month and year.
- Examine descriptive statistics, distributions, monthly/annual summaries, histograms, density plots, and box plots.

### 2. Time series exploration

[`Climatologia_Navojoa_Series_Tiempo.ipynb`](Climatologia_Navojoa_Series_Tiempo.ipynb)

- Index observations by date and inspect time coverage.
- Visualize daily precipitation and minimum/maximum temperatures.
- Zoom into selected historical periods.
- Compare observed temperatures with centered rolling means using windows of **7, 30, and 365 observations**.

> **Interpretation note:** The moving averages use windows of 7, 30, and 365 **observations**, which are not necessarily consecutive calendar days when records are missing. The plots are exploratory, not a statistical test of a climate trend or a forecast.

## Verified visualizations

These figures are calculated directly from the supplied daily station records, grouping **nonmissing daily observations by calendar month**. Unequal coverage across years and months should be considered when interpreting the averages.

### Precipitation by month

![Observed mean daily precipitation by month](reports/figures/monthly_precipitation.svg)

The highest observed mean daily precipitation occurs in **August (3.70 mm/day)**, followed by **July (2.69 mm/day)** and **September (2.34 mm/day)**. These are *average recorded daily precipitation values*, **not** monthly rainfall totals.

### Temperature by month

![Observed mean daily maximum and minimum temperatures by month](reports/figures/monthly_temperatures.svg)

The highest monthly mean of recorded daily maximum temperatures is in **June (38.97 °C)**. The mean recorded daily minimum temperature peaks in **July (23.89 °C)**.

To regenerate the numeric summary and the two SVG charts from the original dataset using only Python's standard library, run:

```bash
python scripts/generate_figures.py
```

The script generates `reports/monthly_summary.csv` and updates both SVG charts. The calculations are documented in [`scripts/generate_figures.py`](scripts/generate_figures.py).

## Descriptive observations

The following are observations from the *supplied reference tables*, not newly calculated results from the notebooks:

- The 1951–2010 **climatological normals file** lists **August** as the wettest month on average (**121.6 mm**) and **May** as the driest (**0.0 mm** in its reported rounded normal).
- That same reference lists an annual normal precipitation of **407.2 mm**.
- The monthly normal maximum temperature peaks in **June (37.2 °C)**, while the monthly normal minimum temperature peaks in **July (23.0 °C)**.

These figures provide climatological context. A comparable summary directly derived from the daily dataset would require documenting coverage and missing-data rules.

## Repository contents

```text
Meteorological-Data-Analysis/
├── BD_Climatologica_Navojoa.ipynb           # Featured EDA (annotated, with figures)
├── Climatologia_Navojoa_Series_Tiempo.ipynb # Featured time-series analysis
├── ClimatologiaNavojoa.txt                  # Daily source observations
├── ExtremosNavojoa.TXT
├── NORMAL26131.TXT
├── README.md
├── archive/
│   └── originals/                           # Historical notebook and script versions
├── scripts/                                 # Reusable analysis and figure-generation code
├── reports/figures/                         # Reproducible summary graphics
├── tests/                                   # Regression tests
└── .github/workflows/validate.yml
```

## Reproduce the analysis

1. Clone the repository:
   ```bash
   git clone https://github.com/ClaudethClarissa/Meteorological-Data-Analysis.git
   cd Meteorological-Data-Analysis
   ```
2. Set up your Python environment (Python 3.11 is used by CI), then install the notebook dependencies:
   ```bash
   python -m pip install notebook numpy pandas matplotlib seaborn statsmodels nbconvert ipykernel
   ```
3. Regenerate the README figures and monthly summary:
   ```bash
   python scripts/generate_figures.py
   ```
4. Open the **two featured notebooks at the repository root**:
   ```bash
   jupyter notebook
   ```
5. Run automated regression tests:
   ```bash
   python -m unittest discover -s tests -v
   ```

GitHub Actions executes both analysis notebooks and regression tests for proposed changes. Historical versions are kept in `archive/originals/` for reference.

## Limitations & planned improvements

- **Incomplete historical coverage:** Missing daily values and differing year/month coverage can bias naive comparisons; validate completeness before making year-to-year or trend claims.
- **Precipitation aggregation:** Daily precipitation averages and monthly/annual precipitation **totals** are different quantities. The featured notebooks now label the corrected annual and monthly mean charts as averages; interpret archived original figures with care, since their historical labels are unchanged.
- **Rolling-window definitions:** Rolling averages are based on observation counts, not guaranteed calendar-day windows when the daily record is incomplete.
- **Data-cleaning robustness:** Further audits of date completeness, invalid records, and unusual observations would improve reliability.
- **Reproducibility:** Both notebooks, supporting scripts, and figure generation are CI-tested. Dependency versions are not yet pinned for long-term preservation.
- **Next analysis:** Compare seasonal patterns across well-observed periods and explicitly quantify completeness before evaluating any long-term trend.

This repository documents an exploratory scientific analysis, **not** a validated climate-change attribution study or operational weather forecast.

---

**Portfolio:** [Data Science & Analytics Portfolio](https://github.com/ClaudethClarissa/data-science-portfolio) · **Author:** [Claudeth Hernandez](https://github.com/ClaudethClarissa)
