"""
CodeCoverageTest_ride_share_fare.py
Lab 6: Code Coverage Test Suite for ride_share_fare.py
Student: Mohammed Sinan (PES1UG24AM165)
Assigned Repository: SETAPESU26/L6_L7_40_ride_share_fare

Objective:
Achieve minimum 90% (achieved: 100%) line/statement coverage on ride_share_fare.py.
This suite ensures every line of executable code is traversed at least once.
"""

import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ==============================================================================
# 1. Tests for extra_distance_fare() line coverage
# ==============================================================================

def test_extra_distance_fare_invalid_cab_type():
    """Traverses lines 5-6 (raises ValueError for unknown cab type)."""
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("auto", 10, "city", False)


def test_extra_distance_fare_negative_distance():
    """Traverses lines 7-8 (raises ValueError for negative distance)."""
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -5, "city", False)


def test_extra_distance_fare_within_included():
    """Traverses lines 9, 10, 12, 13, 14 (returns 0 when extra <= 0)."""
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_extra_distance_fare_subscriber_city():
    """Traverses line 11 (subscriber included bonus), line 15-16 (city rate), line 23."""
    # sedan: 8 + 3 = 11 km included; 15 km -> extra = 4; city rate = 12 -> 4 * 12 = 48
    assert extra_distance_fare("sedan", 15, "city", True) == 48


def test_extra_distance_fare_outstation_surcharge():
    """Traverses line 17-18 (else non-city rate), 19-20 (extra > 20 rate + 8), 21-22 (outstation rate + 4), 23."""
    # suv: 12 km included; distance = 40 -> extra = 28 (>20); rate = 18 + 8 + 4 = 30 -> 28 * 30 = 840
    assert extra_distance_fare("suv", 40, "outstation", False) == 840


# ==============================================================================
# 2. Tests for seats_and_bags_ok() line coverage
# ==============================================================================

def test_seats_and_bags_wheelchair():
    """Traverses lines 27-28 (wheelchair check returns passengers <= 2)."""
    assert seats_and_bags_ok(2, 1, True) is True


def test_seats_and_bags_passenger_limit_exceeded():
    """Traverses lines 29-30 (returns False when passengers > 4)."""
    assert seats_and_bags_ok(5, 1, False) is False


def test_seats_and_bags_standard_ok():
    """Traverses line 31 (returns bags <= 2)."""
    assert seats_and_bags_ok(3, 1, False) is True


# ==============================================================================
# 3. Tests for pickup_status() line coverage
# ==============================================================================

def test_pickup_status_scheduled_airport_delayed():
    """Traverses line 35-36 (scheduled cutoff=10), 39-40 (airport cutoff+=10 -> 20), 43-44 (delayed)."""
    assert pickup_status(15, True, True) == "delayed"


def test_pickup_status_unscheduled_city_on_time():
    """Traverses line 37-38 (else cutoff=5), 41-42 (on_time)."""
    assert pickup_status(10, False, False) == "on_time"


def test_pickup_status_unscheduled_city_missed():
    """Traverses line 45 (missed)."""
    assert pickup_status(-15, False, False) == "missed"
