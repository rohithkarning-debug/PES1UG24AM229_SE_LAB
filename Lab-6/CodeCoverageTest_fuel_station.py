"""Code (line) coverage tests for fuel_station.py.

Goal: execute every line of fuel_station.py at least once.
"""
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# ---------- fuel_bill ----------

def test_within_covered_litres():
    # regular covers 10 litres, 8 requested -> nothing to pay
    assert fuel_bill("regular", 8, "silver") == 0


def test_unknown_grade_raises_error():
    with pytest.raises(ValueError):
        fuel_bill("kerosene", 10, "silver")


def test_negative_litres_raises_error():
    with pytest.raises(ValueError):
        fuel_bill("regular", -5, "silver")


def test_diesel_small_extra():
    # diesel covers 20 litres, 30 requested -> 10 extra at rate 90
    assert fuel_bill("diesel", 30, "silver") == 900


def test_gold_premium_large_extra():
    # gold on premium gets 5 bonus litres -> 20 covered
    # 60 requested -> 40 extra, rate = 105 - 6 - 4 = 95
    assert fuel_bill("premium", 60, "gold") == 3800


# ---------- pump_allowed ----------

def test_pump_allowed():
    assert pump_allowed(30, 1, False) is True


def test_fleet_within_limit():
    assert pump_allowed(150, 5, True) is True


def test_non_fleet_over_60_litres():
    assert pump_allowed(70, 1, False) is False


# ---------- session_status ----------

def test_card_night_active():
    # card cutoff 60 + night 30 = 90, 100 seconds left
    assert session_status(100, True, True) == "active"


def test_cash_warning():
    # cash cutoff 30, warning from 15 to 29 seconds
    assert session_status(20, False, False) == "warning"


def test_cash_timed_out():
    assert session_status(5, False, False) == "timed_out"
