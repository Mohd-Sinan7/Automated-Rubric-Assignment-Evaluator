def parse_plan(text):
    plan, gb = text.split(':')
    return plan.strip().title(), float(gb)

def usage_average(usage_csv):
    values = [int(r) for r in usage_csv.split(',')]
    return sum(values) // len(values)

def payable_bill(text):
    bill, discount = text.split('|')
    total = float(bill) * 1.18 - float(discount)
    return max(total, 0)

def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter plan:data in GB (e.g. standard:5): ")
    result = parse_plan(user_input)
    print("Plan and Data:", result)

    print("\n==== Running usage_average ====")
    user_input = input("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    result = usage_average(user_input)
    print("Average Usage:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 399|50): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)

if __name__ == "__main__":
    main()
