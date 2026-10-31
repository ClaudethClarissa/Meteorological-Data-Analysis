# Historical Climate Analysis | Navojoa, Mexico 🌦️

**Exploratory Data Analysis · Data Cleaning · Time Series Visualization**

A Python-based exploration of historical daily weather observations from **Navojoa (FFCC) station 26131**, Sonora, Mexico. The project studies the seasonal distribution of precipitation and maximum/minimum temperatures, and illustrates how rolling averages reveal patterns at different time scales.

[**Explore the EDA notebook**](BD_Climatologica_Navojoa.ipynb) · [**Explore the time series notebook**](Climatologia_Navojoa_Series_Tiempo.ipynb) · [**Return to my portfolio**](https://github.com/ClaudethClarissa/data-science-portfolio)

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
- What becomes visible when daily temperature series are smoothed with 7-, 30-, and 365-observation rolling means?
- What limitations must be considered when interpreting an incomplete historical record?

## Data source

The daily observations in [`ClimatologiaNavojoa.txt`](ClimatologiaNavojoa.txt) are labeled **CNA–SMN** (Mexico's National Meteorological Service), with a file issue date of April 6, 2020. The file identifies station 26131 as **Navojoa (FFCC)** and notes the station's status as suspended.

Two additional reference files are provided:
- [`ExtremosNavojoa.TXT`](ExtremosNavojoa.TXT): monthly historical extremes and related statistics.
- [`NORMAL26131.TXT`](NORMAL26131.TXT): published climatological normals, labeled **1951–2010**. These reference values should not be treated as estimates from the entire 1931–1993 daily record.

The original file includes an evaporation column, but the analysis omits it because the supplied daily observations do not contain usable evaporation values.

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

> **Interpretation note:** The notebooks use row-based rolling windows, so these are not necessarily continuous 7-, 30-, or 365-calendar-day periods where observations are missing. Rolling averages are descriptive smoothing tools, not fitted climate trends or forecasts.

## Descriptive observations

The following are observations from the *supplied reference tables*, not newly calculated results from the notebooks:

- The 1951–2010 **climatological normals file** lists **August** as the wettest month on average (**121.6 mm**) and **May** as the driest (**0.0 mm** in its reported rounded normal).
- That same reference lists an annual normal precipitation of **407.2 mm**.
- The monthly normal maximum temperature peaks in **June (37.2 °C)**, while the monthly normal minimum temperature peaks in **July (23.0 °C)**.

These figures provide climatological context. A comparable summary directly derived from the daily dataset would require documenting coverage and missing-data rules.

## Repository contents

```text
Meteorological-Data-Analysis/
├── BD_Climatologica_Navojoa.ipynb           # Data cleaning and EDA
├── Climatologia_Navojoa_Series_Tiempo.ipynb  # Time series exploration
├── BD_Climatologica_Navojoa.py              # Script export of EDA notebook
├── Climatologia_Navojoa_Series_Tiempo.py     # Script export of time series notebook
├── ClimatologiaNavojoa.txt                  # Original daily station records
├── ExtremosNavojoa.TXT                      # Historical extremes reference
├── NORMAL26131.TXT                          # Climatological normals reference
└── README.md
```

## How to explore

1. Clone the repository:
   ```bash
   git clone https://github.com/ClaudethClarissa/Meteorological-Data-Analysis.git
   cd Meteorological-Data-Analysis
   ```
2. Install the libraries used in the notebooks:
   ```bash
   python -m pip install notebook numpy pandas matplotlib seaborn statsmodels
   ```
3. Open Jupyter:
   ```bash
   jupyter notebook
   ```
4. Run the EDA notebook first, then the time series notebook. Keep `ClimatologiaNavojoa.txt` in the repository root, because the notebooks use a relative path to load it.

**Compatibility note:** These are original exploratory notebooks; some APIs have changed in newer versions of pandas/NumPy/Seaborn. Reproducibility and dependency pinning are planned improvements, not yet guaranteed.

## Limitations & planned improvements

- **Incomplete historical coverage:** Missing daily values and differing year/month coverage can bias naive comparisons; validate completeness before making year-to-year or trend claims.
- **Precipitation aggregation:** Daily precipitation averages and monthly/annual precipitation **totals** are different quantities. Some existing plot labels should be revised to match the actual calculation.
- **Rolling-window definitions:** Reindex to a continuous daily calendar before calling window sizes “days,” or label them as observation-based windows.
- **Data-cleaning robustness:** Replace row-index-based deletion with content-based filtering, and audit parsing and missingness.
- **Reproducibility:** Add pinned dependencies, documented cleaning logic, tested notebooks, and generated figures.
- **Presentation:** Export a small set of verified, high-resolution plots and add data-supported findings here.

This repository documents an exploratory scientific analysis, **not** a validated climate-change attribution study or operational weather forecast.

---

**Portfolio:** [Data Science & Analytics Portfolio](https://github.com/ClaudethClarissa/data-science-portfolio) · **Author:** [Claudeth Hernandez](https://github.com/ClaudethClarissa)
