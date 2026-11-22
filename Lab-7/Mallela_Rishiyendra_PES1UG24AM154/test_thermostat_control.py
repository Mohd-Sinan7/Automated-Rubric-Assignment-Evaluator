"""Lab 7 - Hypothesis fuzz tests for thermostat_control.py.

Student: Rishyendra M (PES1UG24AM154)
Each function must never crash on arbitrary input (random text or None) and,
for well-formed input, must return a correct value.
Invalid input is expected to return None instead of raising.
"""
import math

from hypothesis import given, settings, strategies as st
from thermostat_control import parse_setpoint, average_temperature, schedule_slot

FUZZ = settings(max_examples=500, deadline=None)
finite = st.floats(min_value=-1000, max_value=1000,
                   allow_nan=False, allow_infinity=False)


# ---------------- parse_setpoint ----------------
@FUZZ
@given(st.text() | st.none())
def test_parse_setpoint_no_crash(s):
    try:
        result = parse_setpoint(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_setpoint crashed with: {e!r}"
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@FUZZ
@given(finite, st.sampled_from(["C", "c", "F", "f"]))
def test_parse_setpoint_valid_values(value, unit):
    result = parse_setpoint(f"{value}{unit}")
    expected = value if unit in "Cc" else (value - 32) * 5 / 9
    assert result is not None
    assert abs(result - round(expected, 1)) <= 0.1


@FUZZ
@given(finite, st.sampled_from(["K", "x", "%", "1", " "]))
def test_parse_setpoint_rejects_unknown_unit(value, unit):
    assert parse_setpoint(f"{value}{unit}") is None


# ---------------- average_temperature ----------------
@FUZZ
@given(st.text() | st.none())
def test_average_temperature_no_crash(s):
    try:
        result = average_temperature(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"average_temperature crashed with: {e!r}"
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@FUZZ
@given(st.lists(finite, min_size=1, max_size=20))
def test_average_temperature_between_min_and_max(values):
    result = average_temperature(",".join(str(v) for v in values))
    assert result is not None
    assert min(values) - 1e-6 <= result <= max(values) + 1e-6


@FUZZ
@given(st.lists(st.sampled_from(["", " ", "nan", "inf", "abc", "-inf"]),
                min_size=1, max_size=5))
def test_average_temperature_rejects_garbage(parts):
    assert average_temperature(",".join(parts)) is None


# ---------------- schedule_slot ----------------
@FUZZ
@given(st.text() | st.none())
def test_schedule_slot_no_crash(s):
    try:
        result = schedule_slot(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"schedule_slot crashed with: {e!r}"
    assert result is None or isinstance(result, str)


@FUZZ
@given(st.integers(0, 23), st.integers(0, 59))
def test_schedule_slot_valid_times(hour, minute):
    result = schedule_slot(f"{hour:02d}:{minute:02d}")
    expected = ("night " if hour < 6 else "day ") + f"{minute:02d}"
    assert result == expected


@FUZZ
@given(st.integers(), st.integers())
def test_schedule_slot_out_of_range_rejected(hour, minute):
    if 0 <= hour <= 23 and 0 <= minute <= 59:
        return
    assert schedule_slot(f"{hour}:{minute}") is None
