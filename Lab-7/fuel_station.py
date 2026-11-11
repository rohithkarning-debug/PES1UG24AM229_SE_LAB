import math
import sys


def parse_purchase(text: str) -> tuple[str, float]:
    if not isinstance(text, str):
        raise TypeError("purchase must be a string")

    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("purchase must contain exactly one ':' separator")

    grade = parts[0].strip()
    if not grade:
        raise ValueError("fuel grade must not be empty")

    try:
        litres = float(parts[1])
    except ValueError as exc:
        raise ValueError("litres must be a valid number") from exc

    if not math.isfinite(litres) or litres < 0:
        raise ValueError("litres must be a finite, non-negative number")

    return grade.title(), litres


def volume_average(volumes_csv: str) -> int:
    if not isinstance(volumes_csv, str):
        raise TypeError("volumes must be a CSV string")

    entries = volumes_csv.split(",")
    try:
        values = [int(entry) for entry in entries]
    except ValueError as exc:
        raise ValueError("volumes must be comma-separated integers") from exc

    if any(value < 0 for value in values):
        raise ValueError("volumes must be non-negative")

    return sum(values) // len(values)


def payable_bill(text: str) -> float:
    if not isinstance(text, str):
        raise TypeError("bill must be a string")

    parts = text.split("|")
    if len(parts) != 2:
        raise ValueError("bill must contain exactly one '|' separator")

    try:
        bill = float(parts[0])
        discount = float(parts[1])
    except ValueError as exc:
        raise ValueError("bill and discount must be valid numbers") from exc

    if not math.isfinite(bill) or bill < 0:
        raise ValueError("bill must be a finite, non-negative number")
    if not math.isfinite(discount) or discount < 0:
        raise ValueError("discount must be a finite, non-negative number")

    taxed_bill = bill * 1.18
    if not math.isfinite(taxed_bill):
        raise ValueError("bill is too large to calculate with 18% tax")

    return max(taxed_bill - discount, 0.0)


def main() -> int:
    print("==== Running parse_purchase ====")
    user_input = input("Enter grade:litres (e.g. diesel:25): ")
    try:
        result = parse_purchase(user_input)
    except ValueError as exc:
        print(f"Invalid purchase: {exc}", file=sys.stderr)
        return 1
    print("Grade and Litres:", result)

    print("\n==== Running volume_average ====")
    user_input = input("Enter pump volumes in litres as CSV (e.g. 10,25,40): ")
    try:
        result = volume_average(user_input)
    except ValueError as exc:
        print(f"Invalid pump volumes: {exc}", file=sys.stderr)
        return 1
    print("Average Volume:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 2500|100): ")
    try:
        result = payable_bill(user_input)
    except ValueError as exc:
        print(f"Invalid bill: {exc}", file=sys.stderr)
        return 1
    print("Payable Bill:", result)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
