import math

GST_RATE = 1.18  # 18% GST is added to the bill before the discount is taken off


def _finite_number(text):
    """float(text) if text is a finite number, otherwise None (bad text, nan, inf, overflow)."""
    try:
        value = float(text)
    except (TypeError, ValueError, OverflowError):
        return None
    return value if math.isfinite(value) else None


def parse_plan(text):
    """'standard:5' -> ('Standard', 5.0). Returns None for invalid input.

    Valid input is a string with exactly one ':', a non-blank plan name and a
    finite, non-negative amount of data in GB.
    """
    if not isinstance(text, str) or text.count(':') != 1:
        return None
    plan, gb = text.split(':')
    plan = plan.strip()
    data_gb = _finite_number(gb)
    if not plan or data_gb is None or data_gb < 0:
        return None
    return plan.title(), data_gb + 0.0  # + 0.0 turns -0.0 into 0.0


def usage_average(usage_csv):
    """'300,450,800' -> 516 (average daily usage in whole MB). Returns None for invalid input.

    Every comma-separated field must be a whole, non-negative number of MB;
    empty fields, words, decimals and over-long numbers are rejected.
    """
    if not isinstance(usage_csv, str):
        return None
    values = []
    for field in usage_csv.split(','):
        try:
            value = int(field)
        except ValueError:  # '', 'abc', '1.5', more than 4300 digits ...
            return None
        if value < 0:
            return None
        values.append(value)
    if not values:
        return None
    return sum(values) // len(values)


def payable_bill(text):
    """'399|50' -> 420.82 (bill + 18% GST - discount, never below 0). Returns None for invalid input.

    Valid input is a string with exactly one '|' between two finite,
    non-negative amounts. The result is rounded to paise (2 decimals).
    """
    if not isinstance(text, str) or text.count('|') != 1:
        return None
    bill_text, discount_text = text.split('|')
    bill = _finite_number(bill_text)
    discount = _finite_number(discount_text)
    if bill is None or discount is None or bill < 0 or discount < 0:
        return None
    total = bill * GST_RATE - discount
    if not math.isfinite(total):  # e.g. 1e308 * 1.18 overflows to inf
        return None
    return round(total, 2) if total > 0 else 0.0


def _ask(prompt):
    """input() that treats a closed stdin (EOF) as an empty answer instead of crashing."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return ""


def main():
    print("==== Running parse_plan ====")
    user_input = _ask("Enter plan:data in GB (e.g. standard:5): ")
    result = parse_plan(user_input)
    if result is None:
        print("Invalid input: expected plan:data in GB, e.g. standard:5 (data must be a number >= 0)")
    else:
        print("Plan and Data:", result)

    print("\n==== Running usage_average ====")
    user_input = _ask("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    result = usage_average(user_input)
    if result is None:
        print("Invalid input: expected whole numbers of MB >= 0 separated by commas, e.g. 300,450,800")
    else:
        print("Average Usage:", result)

    print("\n==== Running payable_bill ====")
    user_input = _ask("Enter bill|discount (e.g. 399|50): ")
    result = payable_bill(user_input)
    if result is None:
        print("Invalid input: expected bill|discount with two amounts >= 0, e.g. 399|50")
    else:
        print("Payable Bill:", result)


if __name__ == "__main__":
    main()
