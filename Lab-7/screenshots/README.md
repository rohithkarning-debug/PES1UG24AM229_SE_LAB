# Screenshot checklist

The four genuine terminal screenshots below are included as captured. Do not
edit or fabricate terminal output. Each image should show the command, inputs,
and relevant result.

- [x] [Original buggy application](./01_original_application.png) — run `python fuel_station_buggy.py`
  and enter valid sample inputs at all three prompts.
- [x] [Failing Hypothesis tests](./02_failing_hypothesis_tests.png) — run the test suite against the preserved
  original implementation:

  ```powershell
  python -c "import sys; import fuel_station_buggy; sys.modules['fuel_station'] = fuel_station_buggy; import pytest; raise SystemExit(pytest.main(['-v', 'test_fuel_station.py']))"
  ```

- [x] [Fixed application](./03_fixed_application.png) — run `python fuel_station.py` and enter
  valid sample inputs at all three prompts.
- [x] [Final successful pytest execution](./04_all_tests_passing.png) — run
  `python -m pytest -v test_fuel_station.py`.

All four screenshots are also embedded in the submission PDF.
