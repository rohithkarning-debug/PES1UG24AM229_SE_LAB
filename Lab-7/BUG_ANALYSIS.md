# Bug analysis

## Baseline run

The preserved `fuel_station_buggy.py` was loaded as the `fuel_station` module
so the unchanged pytest suite exercised the original implementation:

```powershell
python -c "import sys; import fuel_station_buggy; sys.modules['fuel_station'] = fuel_station_buggy; import pytest; raise SystemExit(pytest.main(['-v', 'test_fuel_station.py']))"
```

Observed result: **17 failed, 24 passed**. Four failures came from Hypothesis
generated properties; the rest came from explicit edge cases.

## Failures and counterexamples

| Function | Observed input | Defect |
|----------|----------------|--------|
| `parse_purchase` | `:25` | Accepted a purchase with an empty fuel grade. |
| `parse_purchase` | `diesel:-1` | Accepted a negative purchase volume. Hypothesis also minimized this to `litres=-1.0`. |
| `parse_purchase` | `diesel:nan`, `diesel:inf` | Accepted non-finite fuel volumes. |
| `volume_average` | `-1` | Accepted a negative pump volume. Hypothesis minimized this to `volume=-1`. |
| `payable_bill` | `-1|0`, `100|-1` | Accepted a negative bill or discount. Hypothesis minimized these to `bill=-1.0` and `discount=-1.0`. |
| `payable_bill` | `nan|0`, `inf|0`, `100|nan` | Accepted non-finite amounts, allowing invalid numeric results. |
| `payable_bill` | `1.7e308|0` | The 18% calculation overflowed to infinity and was returned instead of rejected. |
| All three functions | `None` | Raised `AttributeError` while calling `.split()` instead of the expected `TypeError` for a non-string argument. |
| Interactive application | `:25` at the purchase prompt | An invalid value propagated as a traceback. The fixed CLI now displays a concise validation error and exits with status 1. This was found by a manual smoke test, not counted among the pytest baseline failures. |

The fixes validate input types, delimiters, non-empty grades, non-negative
values, and finite numeric results. `volume_average` retains the original
integer-floor average behavior; `payable_bill` retains 18% tax followed by the
discount and a zero lower bound. CLI input validation errors are reported
without a traceback.
