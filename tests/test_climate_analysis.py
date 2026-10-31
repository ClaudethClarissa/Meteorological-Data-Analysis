"""Regression tests against the supplied original daily observations."""
import csv
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_figures as climate


class ClimateAnalysisTests(unittest.TestCase):
    def test_monthly_averages_and_nonmissing_counts(self):
        monthly = climate.monthly_statistics()
        self.assertEqual(len(monthly), 12)
        self.assertEqual(sum(row["n_precip"] for row in monthly), 13370)
        self.assertEqual(sum(row["n_tmax"] for row in monthly), 13322)
        self.assertEqual(sum(row["n_tmin"] for row in monthly), 13293)
        self.assertAlmostEqual(monthly[7]["precip"], 3.696, delta=0.005)
        self.assertAlmostEqual(monthly[5]["tmax"], 38.97, delta=0.01)
        self.assertAlmostEqual(monthly[6]["tmin"], 23.89, delta=0.01)

    def test_svg_charts_parse(self):
        summary = climate.monthly_statistics()
        for drawing in (climate.precipitation_chart(summary),
                        climate.temperature_chart(summary)):
            root = ET.fromstring(drawing)
            self.assertTrue(root.tag.endswith("svg"))

    def test_export_generates_all_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(climate, "ROOT", Path(tmp)):
                # Use an exact copy of the original file, never mutate it.
                (Path(tmp) / "ClimatologiaNavojoa.txt").write_bytes(
                    (ROOT / "ClimatologiaNavojoa.txt").read_bytes()
                )
                climate.main()
                csv_file = Path(tmp) / "reports" / "monthly_summary.csv"
                self.assertTrue(csv_file.is_file())
                with csv_file.open(newline="", encoding="utf-8") as stream:
                    rows = list(csv.DictReader(stream))
                self.assertEqual(len(rows), 12)
                for name in ("monthly_precipitation.svg", "monthly_temperatures.svg"):
                    ET.parse(Path(tmp) / "reports" / "figures" / name)


if __name__ == "__main__":
    unittest.main()
