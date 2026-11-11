def parse_purchase(text):
    grade, litres = text.split(':')
    return grade.strip().title(), float(litres)

def volume_average(volumes_csv):
    values = [int(r) for r in volumes_csv.split(',')]
    return sum(values) // len(values)

def payable_bill(text):
    bill, discount = text.split('|')
    total = float(bill) * 1.18 - float(discount)
    return max(total, 0)

def main():
    print("==== Running parse_purchase ====")
    user_input = input("Enter grade:litres (e.g. diesel:25): ")
    result = parse_purchase(user_input)
    print("Grade and Litres:", result)

    print("\n==== Running volume_average ====")
    user_input = input("Enter pump volumes in litres as CSV (e.g. 10,25,40): ")
    result = volume_average(user_input)
    print("Average Volume:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 2500|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)

if __name__ == "__main__":
    main()
