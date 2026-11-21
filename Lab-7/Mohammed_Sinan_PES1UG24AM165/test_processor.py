"""Property-based fuzz testing and unit tests using Hypothesis for Ride Share Fare."""

import pytest
from hypothesis import given, strategies as st
from processor import parse_trip, fare_average, payable_fare


# ---------------------------------------------------------------------------
# 1. Hypothesis Fuzz Tests (Random/Malformed Inputs - No Crash Guarantees)
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_trip_no_crash(s):
    """Fuzz test: parse_trip must never raise an unhandled exception on any input."""
    try:
        result = parse_trip(s)
        if result is not None:
            assert isinstance(result, tuple)
            assert len(result) == 2
            assert isinstance(result[0], str)
            assert isinstance(result[1], (int, float))
            assert result[1] >= 0
    except Exception as e:
        assert False, f"parse_trip crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_fare_average_no_crash(s):
    """Fuzz test: fare_average must never raise an unhandled exception on any input."""
    try:
        result = fare_average(s)
        assert isinstance(result, int)
        assert result >= 0
    except Exception as e:
        assert False, f"fare_average crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_payable_fare_no_crash(s):
    """Fuzz test: payable_fare must never raise an unhandled exception on any input."""
    try:
        result = payable_fare(s)
        assert isinstance(result, (int, float))
        assert result >= 0
    except Exception as e:
        assert False, f"payable_fare crashed with {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 2. Targeted Property-Based Tests (Valid Input Distributions)
# ---------------------------------------------------------------------------

@given(
    cab=st.text(alphabet=st.characters(categories=["L", "N"]), min_size=1, max_size=20),
    km=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False)
)
def test_parse_trip_valid_inputs(cab, km):
    """Verify parse_trip produces correct title-cased cab and float distance."""
    formatted = f"{cab}:{km}"
    result = parse_trip(formatted)
    assert result is not None
    assert result[0] == cab.strip().title()
    assert abs(result[1] - km) < 1e-4


@given(st.lists(st.integers(min_value=1, max_value=10000), min_size=1, max_size=50))
def test_fare_average_valid_lists(fare_list):
    """Verify fare_average calculates the integer average correctly for valid CSV."""
    csv_str = ",".join(str(f) for f in fare_list)
    result = fare_average(csv_str)
    expected = sum(fare_list) // len(fare_list)
    assert result == expected


@given(
    fare=st.floats(min_value=1.0, max_value=5000.0, allow_nan=False, allow_infinity=False),
    promo=st.floats(min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False)
)
def test_payable_fare_valid_formula(fare, promo):
    """Verify payable_fare satisfies total = max(fare * 1.18 - promo, 0.0)."""
    text = f"{fare}|{promo}"
    result = payable_fare(text)
    expected = max(fare * 1.18 - promo, 0.0)
    assert abs(result - expected) < 1e-4


# ---------------------------------------------------------------------------
# 3. Deterministic Edge Case Unit Tests
# ---------------------------------------------------------------------------

def test_parse_trip_edge_cases():
    """Verify edge cases discovered during fuzzing return None safely."""
    assert parse_trip(None) is None
    assert parse_trip("") is None
    assert parse_trip(":") is None
    assert parse_trip("::") is None
    assert parse_trip("sedan:not_a_number") is None
    assert parse_trip("sedan:-15") is None
    assert parse_trip("   : 10") is None
    assert parse_trip("sedan:10:extra") is None
    assert parse_trip("sedan:12") == ("Sedan", 12.0)


def test_fare_average_edge_cases():
    """Verify fare_average edge cases handle empty, non-numeric, and whitespace inputs."""
    assert fare_average(None) == 0
    assert fare_average("") == 0
    assert fare_average(",,,") == 0
    assert fare_average("invalid,tokens") == 0
    assert fare_average("120,95,210") == 141
    assert fare_average(" 100 , 200 ") == 150


def test_payable_fare_edge_cases():
    """Verify payable_fare edge cases handle missing separators, large promos, and negatives."""
    assert payable_fare(None) == 0.0
    assert payable_fare("") == 0.0
    assert payable_fare("|") == 0.0
    assert payable_fare("250|") == 0.0
    assert payable_fare("|30") == 0.0
    assert payable_fare("250|30") == 265.0
    assert payable_fare("100|500") == 0.0  # Promo exceeds fare with tax
    assert payable_fare("-100|20") == 0.0  # Negative fare rejected

