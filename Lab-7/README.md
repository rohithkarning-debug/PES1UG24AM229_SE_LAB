# L6_L7_47 — Fuel Station

Lab 7: Fuzz Testing with Hypothesis and pytest.

## About

This module parses fuel purchases, computes the average of pump volumes, and
calculates the payable bill using 18% tax followed by a discount.

## Files

| File | Description |
|------|-------------|
| `fuel_station.py` | Validated implementation and interactive application |
| `fuel_station_buggy.py` | Original implementation, preserved for comparison |
| `test_fuel_station.py` | Example-based and Hypothesis property tests |
| `BUG_ANALYSIS.md` | Baseline defects and the observed failing cases |
| `requirements.txt` | pytest and Hypothesis test dependencies |
| `.gitignore` | Excludes Python, pytest, and Hypothesis caches |
| `PES1UG24AM229_Lab7.pdf` | Four-page submission with the original screenshots |
| `screenshots/` | Genuine application and test-run evidence |

## Input rules

- `parse_purchase(text)` accepts `grade:litres`; the grade must not be empty,
  and litres must be a finite, non-negative number.
- `volume_average(volumes_csv)` accepts one or more comma-separated,
  non-negative integers. It returns the integer floor of their arithmetic
  mean, preserving the original application's integer-average behavior.
- `payable_bill(text)` accepts `bill|discount`; both values must be finite and
  non-negative. It returns `max(bill * 1.18 - discount, 0)`.
- Non-string arguments raise `TypeError`. Malformed, negative, or non-finite
  values raise `ValueError`.
- The interactive application displays validation errors without a traceback
  and exits with status 1 for invalid input.

## Setup and run

From this directory:

```powershell
python -m pip install -r requirements.txt
python fuel_station.py
python -m pytest -v test_fuel_station.py
```

The application prompts for a purchase, pump volumes, and a bill with
discount. `BUG_ANALYSIS.md` documents the original failures found by running
the same test suite against `fuel_station_buggy.py`.
