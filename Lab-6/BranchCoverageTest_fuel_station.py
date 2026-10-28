"""Branch coverage tests for fuel_station.py.

Goal: make every decision in fuel_station.py go both ways
(True and False), and check the boundary values of each condition.
"""
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# ---------- fuel_bill ----------
# Branches: unknown grade, negative litres, gold bonus (gold AND not diesel),
# extra <= 0, diesel vs petrol rate, extra > 30, gold extra discount.

def test_unknown_grade_raises_error():
    with pytest.raises(ValueError):
        fuel_bill("kerosene", 10, "silver")


def test_negative_litres_raises_error():
    with pytest.raises(ValueError):
        fuel_bill("regular", -1, "silver")


def test_zero_litres_is_free():
    # litres = 0 is valid (litres < 0 is False)
    assert fuel_bill("regular", 0, "silver") == 0


def test_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0


def test_exactly_covered_litres_is_free():
    # extra == 0 -> extra <= 0 is True
    assert fuel_bill("premium", 15, "silver") == 0


def test_one_litre_over_regular():
    # extra == 1 -> extra <= 0 is False, petrol rate 105
    assert fuel_bill("regular", 11, "silver") == 105


def test_gold_bonus_on_petrol():
    # gold AND not diesel -> True: regular covers 10 + 5 = 15 litres
    assert fuel_bill("regular", 15, "gold") == 0
    assert fuel_bill("regular", 16, "gold") == 105


def test_gold_on_diesel_gets_no_bonus():
    # gold but diesel -> condition False, still 20 covered
    # 25 litres -> 5 extra at rate 90
    assert fuel_bill("diesel", 25, "gold") == 450


def test_diesel_small_extra():
    assert fuel_bill("diesel", 30, "silver") == 900


def test_extra_exactly_30_no_bulk_discount():
    # extra == 30 -> extra > 30 is False, full rate 105
    assert fuel_bill("regular", 40, "silver") == 3150


def test_bulk_discount_non_gold():
    # extra 31 -> extra > 30 True, not gold -> rate 105 - 6 = 99
    assert fuel_bill("regular", 41, "silver") == 31 * 99


def test_bulk_discount_gold_petrol():
    # premium gold covers 20, 60 litres -> 40 extra
    # rate = 105 - 6 - 4 = 95
    assert fuel_bill("premium", 60, "gold") == 3800


def test_bulk_discount_gold_diesel():
    # diesel gold: no bonus litres, 60 litres -> 40 extra
    # rate = 90 - 6 - 4 = 80
    assert fuel_bill("diesel", 60, "gold") == 3200


def test_bulk_discount_diesel_non_gold():
    # rate = 90 - 6 = 84
    assert fuel_bill("diesel", 60, "silver") == 40 * 84


# ---------- pump_allowed ----------
# Branches: is_fleet, litres_requested > 60, containers <= 1.

@pytest.mark.parametrize("litres, containers, expected", [
    (200, 10, True),    # fleet at the 200 litre limit
    (201, 0, False),    # fleet just over the limit
])
def test_fleet_limits(litres, containers, expected):
    assert pump_allowed(litres, containers, True) is expected


@pytest.mark.parametrize("litres, containers, expected", [
    (60, 1, True),      # exactly 60 litres is allowed
    (61, 0, False),     # over 60 litres is refused
    (30, 0, True),      # no containers
    (30, 1, True),      # one container is allowed
    (30, 2, False),     # more than one container is refused
])
def test_non_fleet_rules(litres, containers, expected):
    assert pump_allowed(litres, containers, False) is expected


# ---------- session_status ----------
# Branches: card vs cash cutoff, night extension,
# active / warning / timed_out.

@pytest.mark.parametrize("seconds, card, night, expected", [
    # cash, day -> cutoff 30, warning from 15
    (30, False, False, "active"),
    (29, False, False, "warning"),
    (15, False, False, "warning"),
    (14, False, False, "timed_out"),
    # card, day -> cutoff 60, warning from 45
    (60, True, False, "active"),
    (59, True, False, "warning"),
    (45, True, False, "warning"),
    (44, True, False, "timed_out"),
    # cash, night -> cutoff 60
    (60, False, True, "active"),
    (50, False, True, "warning"),
    (10, False, True, "timed_out"),
    # card, night -> cutoff 90, warning from 75
    (90, True, True, "active"),
    (75, True, True, "warning"),
    (74, True, True, "timed_out"),
])
def test_session_status(seconds, card, night, expected):
    assert session_status(seconds, card, night) == expected
