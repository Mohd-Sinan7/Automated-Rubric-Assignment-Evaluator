"""Smart Thermostat Controller (Lab 7 - hardened after fuzz testing).

Student: Rishyendra M (PES1UG24AM154)

Every public function validates its input and returns None for anything it
cannot interpret, instead of raising an unhandled exception.
"""
import math

MAX_INPUT_LENGTH = 10_000   # guard against huge inputs (DoS)
MIN_TEMP_C = -1000.0       # reject absurd setpoints
MAX_TEMP_C = 1000.0


def _to_finite_float(text):
    """Convert text to a finite float, or return None."""
    try:
        value = float(text)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(value):
        return None
    return value


def parse_setpoint(text):
    """Parse '21.5C' / '70F' into degrees Celsius (1 decimal), else None."""
    if not isinstance(text, str) or len(text) > MAX_INPUT_LENGTH:
        return None
    text = text.strip()
    if len(text) < 2:
        return None
    unit = text[-1].upper()
    if unit not in ("C", "F"):
        return None
    value = _to_finite_float(text[:-1])
    if value is None:
        return None
    if unit == "F":
        value = (value - 32) * 5 / 9
    if not MIN_TEMP_C <= value <= MAX_TEMP_C:
        return None
    return float(round(value, 1))


def average_temperature(readings_csv):
    """Average a CSV list of readings such as '20.5,21,22.5', else None."""
    if not isinstance(readings_csv, str) or len(readings_csv) > MAX_INPUT_LENGTH:
        return None
    parts = [p.strip() for p in readings_csv.split(",")]
    if not parts or any(p == "" for p in parts):
        return None
    values = []
    for part in parts:
        value = _to_finite_float(part)
        if value is None:
            return None
        values.append(value)
    result = math.fsum(values) / len(values)
    if not math.isfinite(result):
        return None
    return float(result)


def schedule_slot(time_text):
    """Label an 'HH:MM' time as 'night MM' (before 06:00) or 'day MM'."""
    if not isinstance(time_text, str) or len(time_text) > 16:
        return None
    pieces = time_text.strip().split(":")
    if len(pieces) != 2:
        return None
    hour_text, minute_text = pieces
    if not (hour_text.isascii() and hour_text.isdigit()
            and minute_text.isascii() and minute_text.isdigit()):
        return None
    hour, minute = int(hour_text), int(minute_text)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    prefix = "night" if hour < 6 else "day"
    return f"{prefix} {minute:02d}"


def main():
    """Interactive demo of the three functions."""
    print("==== Running parse_setpoint ====")
    user_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    result = parse_setpoint(user_input)
    print("Setpoint in Celsius:", result if result is not None else "Invalid setpoint")

    print("\n==== Running average_temperature ====")
    user_input = input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): ")
    result = average_temperature(user_input)
    print("Average Temperature:", result if result is not None else "Invalid readings")

    print("\n==== Running schedule_slot ====")
    user_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    result = schedule_slot(user_input)
    print("Schedule Slot:", result if result is not None else "Invalid time")


if __name__ == "__main__":
    main()
