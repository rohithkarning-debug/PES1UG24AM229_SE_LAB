import math
from collections.abc import Callable

import pytest
from hypothesis import given, strategies as st

from fuel_station import parse_purchase, payable_bill, volume_average


_GRADES = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
    min_size=1,
    max_size=30,
).filter(lambda grade: bool(grade.strip()))
_AMOUNTS = st.floats(
    min_value=0,
    max_value=1_000_000_000,
    allow_nan=False,
    allow_infinity=False,
)


@given(grade=_GRADES, litres=_AMOUNTS)
def test_parse_purchase_valid_values(grade: str, litres: float) -> None:
    parsed_grade, parsed_litres = parse_purchase(f"{grade}:{litres}")

    assert parsed_grade == grade.strip().title()
    assert parsed_litres == litres


@given(litres=st.floats(max_value=-0.001, allow_nan=False, allow_infinity=False))
def test_parse_purchase_rejects_negative_litres(litres: float) -> None:
    with pytest.raises(ValueError):
        parse_purchase(f"diesel:{litres}")


@given(text=st.text())
def test_parse_purchase_arbitrary_text_is_valid_or_rejected(text: str) -> None:
    try:
        grade, litres = parse_purchase(text)
    except ValueError:
        return

    original_grade, original_litres = text.split(":")
    expected_litres = float(original_litres)
    assert text.count(":") == 1
    assert original_grade.strip()
    assert grade == original_grade.strip().title()
    assert math.isfinite(litres)
    assert expected_litres >= 0
    assert litres == expected_litres


@pytest.mark.parametrize(
    "text",
    [
        "",
        ":",
        "diesel:",
        ":25",
        "diesel:abc",
        "diesel:-1",
        "diesel:nan",
        "diesel:inf",
        "diesel:1e309",
        "diesel:1:2",
    ],
)
def test_parse_purchase_rejects_invalid_values(text: str) -> None:
    with pytest.raises(ValueError):
        parse_purchase(text)


@given(volumes=st.lists(st.integers(min_value=0, max_value=1_000_000), min_size=1))
def test_volume_average_valid_values(volumes: list[int]) -> None:
    volumes_csv = ",".join(str(volume) for volume in volumes)

    assert volume_average(volumes_csv) == sum(volumes) // len(volumes)


@given(volume=st.integers(max_value=-1))
def test_volume_average_rejects_negative_volumes(volume: int) -> None:
    with pytest.raises(ValueError):
        volume_average(str(volume))


@given(text=st.text())
def test_volume_average_arbitrary_text_is_valid_or_rejected(text: str) -> None:
    try:
        average = volume_average(text)
    except ValueError:
        return

    values = [int(entry) for entry in text.split(",")]
    assert all(value >= 0 for value in values)
    assert average == sum(values) // len(values)


@pytest.mark.parametrize(
    "text",
    ["", ",", "10,,20", "10,", "-1", "1.5", "abc"],
)
def test_volume_average_rejects_invalid_values(text: str) -> None:
    with pytest.raises(ValueError):
        volume_average(text)


@given(bill=_AMOUNTS, discount=_AMOUNTS)
def test_payable_bill_applies_tax_and_discount(bill: float, discount: float) -> None:
    expected = max(bill * 1.18 - discount, 0.0)

    assert payable_bill(f"{bill}|{discount}") == pytest.approx(expected)


@given(bill=st.floats(max_value=-0.001, allow_nan=False, allow_infinity=False))
def test_payable_bill_rejects_negative_bill(bill: float) -> None:
    with pytest.raises(ValueError):
        payable_bill(f"{bill}|0")


@given(discount=st.floats(max_value=-0.001, allow_nan=False, allow_infinity=False))
def test_payable_bill_rejects_negative_discount(discount: float) -> None:
    with pytest.raises(ValueError):
        payable_bill(f"100|{discount}")


@given(text=st.text())
def test_payable_bill_arbitrary_text_is_valid_or_rejected(text: str) -> None:
    try:
        payable = payable_bill(text)
    except ValueError:
        return

    bill_text, discount_text = text.split("|")
    bill = float(bill_text)
    discount = float(discount_text)
    assert text.count("|") == 1
    assert math.isfinite(bill) and bill >= 0
    assert math.isfinite(discount) and discount >= 0
    assert math.isclose(
        payable,
        max(bill * 1.18 - discount, 0.0),
        rel_tol=1e-12,
        abs_tol=1e-9,
    )


@pytest.mark.parametrize(
    "text",
    [
        "",
        "100",
        "100|20|5",
        "abc|5",
        "100|abc",
        "-1|0",
        "100|-1",
        "nan|0",
        "inf|0",
        "100|nan",
        "1.7e308|0",
    ],
)
def test_payable_bill_rejects_invalid_values(text: str) -> None:
    with pytest.raises(ValueError):
        payable_bill(text)


def test_payable_bill_returns_zero_when_discount_exceeds_taxed_bill() -> None:
    assert payable_bill("2500|4000") == 0.0


def test_payable_bill_tax_then_discount_example() -> None:
    assert payable_bill("2500|100") == pytest.approx(2850.0)


def test_none_input_raises_type_error() -> None:
    functions: tuple[Callable[..., object], ...] = (
        parse_purchase,
        volume_average,
        payable_bill,
    )
    for function in functions:
        with pytest.raises(TypeError):
            function(None)
