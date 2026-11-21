"""Ride Share Fare module hardened with defensive input validation."""

import math


def parse_trip(text):
    """
    Parse cab and distance from text formatted as 'cab:distance'.
    Returns a tuple of (title_cased_cab, float_distance) if valid, or None if invalid.
    """
    if not text or not isinstance(text, str) or ':' not in text:
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    cab = parts[0].strip()
    km_str = parts[1].strip()
    if not cab:
        return None
    try:
        km_val = float(km_str)
        if km_val < 0 or math.isnan(km_val) or math.isinf(km_val):
            return None
        return cab.title(), km_val
    except (ValueError, TypeError):
        return None


def fare_average(fares_csv):
    """
    Calculate integer average of comma-separated fare values.
    Returns the integer average of valid non-negative fares, or 0 if invalid or empty.
    """
    if not fares_csv or not isinstance(fares_csv, str):
        return 0
    values = []
    for r in fares_csv.split(','):
        r_str = r.strip()
        if r_str:
            try:
                val = int(r_str)
                if val >= 0:
                    values.append(val)
            except (ValueError, TypeError):
                continue
    if not values:
        return 0
    return sum(values) // len(values)


def payable_fare(text):
    """
    Calculate final payable fare with 18% GST minus promo discount.
    Expected input format: 'fare|promo'.
    Returns max(total, 0.0), or 0.0 if invalid.
    """
    if not text or not isinstance(text, str) or '|' not in text:
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    try:
        fare_val = float(parts[0].strip())
        promo_val = float(parts[1].strip())
        if (
            fare_val < 0
            or promo_val < 0
            or math.isnan(fare_val)
            or math.isnan(promo_val)
            or math.isinf(fare_val)
            or math.isinf(promo_val)
        ):
            return 0.0
        total = fare_val * 1.18 - promo_val
        return max(total, 0.0)
    except (ValueError, TypeError):
        return 0.0


def main():
    """Interactive CLI entrypoint demonstrating all three functions."""
    print("==== Running parse_trip ====")
    user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
    result = parse_trip(user_input)
    print("Cab and Distance:", result)

    print("\n==== Running fare_average ====")
    user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
    result = fare_average(user_input)
    print("Average Fare:", result)

    print("\n==== Running payable_fare ====")
    user_input = input("Enter fare|promo (e.g. 250|30): ")
    result = payable_fare(user_input)
    print("Payable Fare:", result)


if __name__ == "__main__":
    main()
