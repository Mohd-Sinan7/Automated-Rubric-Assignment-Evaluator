"""
BranchCoverageTest_ride_share_fare.py
Lab 6: Branch Coverage Test Suite for ride_share_fare.py
Student: Mohammed Sinan (PES1UG24AM165)
Assigned Repository: SETAPESU26/L6_L7_40_ride_share_fare

Objective:
Achieve minimum 90% (achieved: 100%) branch coverage on ride_share_fare.py.
This suite ensures every decision branch (if/elif/else conditions evaluate
to both True and False, including compound logical expressions) is traversed.
"""

import pytest
from ride_share_fare import extra_distance_fare, seats_and_bags_ok, pickup_status


# ==============================================================================
# 1. Decision & Branch Coverage Tests for extra_distance_fare()
# ==============================================================================

def test_extra_distance_fare_invalid_cab_type():
    """Branch: cab_type not in INCLUDED_KM -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("auto_rickshaw", 10, "city", False)


def test_extra_distance_fare_negative_distance():
    """Branch: distance_km < 0 -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_extra_distance_fare_zero_distance():
    """Branch: distance_km == 0 -> extra <= 0 -> returns 0."""
    assert extra_distance_fare("sedan", 0, "city", False) == 0


def test_extra_distance_fare_exact_included_distance():
    """Branch: distance_km == included -> extra <= 0 -> returns 0."""
    assert extra_distance_fare("mini", 5, "city", False) == 0


def test_extra_distance_fare_less_than_included_distance():
    """Branch: distance_km < included -> extra < 0 -> returns 0."""
    assert extra_distance_fare("mini", 3, "city", False) == 0


def test_extra_distance_fare_subscriber_mini():
    """
    Branch: is_subscriber=True and cab_type != 'suv' -> (True and True -> True).
    Included km increases by 3 for mini (5 + 3 = 8 km).
    """
    # distance = 10 -> extra = 2. City rate = 12. Fare = 2 * 12 = 24.
    assert extra_distance_fare("mini", 10, "city", True) == 24


def test_extra_distance_fare_subscriber_sedan():
    """
    Branch: is_subscriber=True and cab_type != 'suv' -> (True and True -> True).
    Included km increases by 3 for sedan (8 + 3 = 11 km).
    """
    # distance = 21 -> extra = 10 (<= 20). City rate = 12. Fare = 10 * 12 = 120.
    assert extra_distance_fare("sedan", 21, "city", True) == 120


def test_extra_distance_fare_subscriber_suv():
    """
    Branch: is_subscriber=True and cab_type != 'suv' -> (True and False -> False).
    Compound condition evaluates to False; SUV included remains 12 km.
    """
    # distance = 22 -> extra = 10 (<= 20). City rate = 12. Fare = 10 * 12 = 120.
    assert extra_distance_fare("suv", 22, "city", True) == 120


def test_extra_distance_fare_non_subscriber_sedan():
    """Branch: is_subscriber=False -> False condition; included remains 8 km."""
    # distance = 18 -> extra = 10 (<= 20). City rate = 12. Fare = 10 * 12 = 120.
    assert extra_distance_fare("sedan", 18, "city", False) == 120


def test_extra_distance_fare_suburban_non_city_rate():
    """Branch: zone != 'city' -> False branch of zone == 'city', rate = 18."""
    # mini included = 5. distance = 15 -> extra = 10 (<= 20). Suburban rate = 18.
    # Fare = 10 * 18 = 180.
    assert extra_distance_fare("mini", 15, "suburban", False) == 180


def test_extra_distance_fare_extra_gt_20_city():
    """
    Branch: extra > 20 -> True; zone == 'outstation' -> False.
    rate = 12 + 8 = 20 (does NOT add outstation 4).
    """
    # mini included = 5. distance = 30 -> extra = 25 (> 20). City rate = 20.
    # Fare = 25 * 20 = 500.
    assert extra_distance_fare("mini", 30, "city", False) == 500


def test_extra_distance_fare_extra_gt_20_outstation():
    """
    Branch: extra > 20 -> True; zone == 'outstation' -> True.
    rate = 18 + 8 + 4 = 30.
    """
    # sedan included = 8. distance = 33 -> extra = 25 (> 20).
    # Outstation rate = 30. Fare = 25 * 30 = 750.
    assert extra_distance_fare("sedan", 33, "outstation", False) == 750


def test_extra_distance_fare_extra_gt_20_other_zone():
    """
    Branch: extra > 20 -> True; zone == 'highway' (not outstation).
    rate = 18 + 8 = 26.
    """
    # suv included = 12. distance = 37 -> extra = 25 (> 20).
    # Fare = 25 * 26 = 650.
    assert extra_distance_fare("suv", 37, "highway", False) == 650


# ==============================================================================
# 2. Decision & Branch Coverage Tests for seats_and_bags_ok()
# ==============================================================================

def test_seats_and_bags_wheelchair_passengers_le_2():
    """Branch: needs_wheelchair=True -> True; passengers <= 2 -> True."""
    assert seats_and_bags_ok(1, 0, True) is True
    assert seats_and_bags_ok(2, 4, True) is True


def test_seats_and_bags_wheelchair_passengers_gt_2():
    """Branch: needs_wheelchair=True -> True; passengers <= 2 -> False."""
    assert seats_and_bags_ok(3, 0, True) is False


def test_seats_and_bags_passengers_gt_4():
    """Branch: needs_wheelchair=False -> False; passengers > 4 -> True (returns False)."""
    assert seats_and_bags_ok(5, 1, False) is False
    assert seats_and_bags_ok(6, 0, False) is False


def test_seats_and_bags_passengers_le_4_bags_le_2():
    """Branch: needs_wheelchair=False -> False; passengers <= 4 -> False; bags <= 2 -> True."""
    assert seats_and_bags_ok(4, 2, False) is True
    assert seats_and_bags_ok(3, 0, False) is True


def test_seats_and_bags_passengers_le_4_bags_gt_2():
    """Branch: needs_wheelchair=False -> False; passengers <= 4 -> False; bags <= 2 -> False."""
    assert seats_and_bags_ok(4, 3, False) is False


# ==============================================================================
# 3. Decision & Branch Coverage Tests for pickup_status()
# ==============================================================================

def test_pickup_status_scheduled_airport_branches():
    """
    Cutoff calculation:
    is_scheduled=True -> cutoff = 10
    is_airport=True   -> cutoff += 10 -> total cutoff = 20
    """
    # Branch: minutes_early >= cutoff (20) -> "on_time"
    assert pickup_status(25, True, True) == "on_time"
    assert pickup_status(20, True, True) == "on_time"
    # Branch: minutes_early >= cutoff - 15 (5) and < 20 -> "delayed"
    assert pickup_status(19, True, True) == "delayed"
    assert pickup_status(5, True, True) == "delayed"
    # Branch: minutes_early < 5 -> "missed"
    assert pickup_status(4, True, True) == "missed"
    assert pickup_status(-1, True, True) == "missed"


def test_pickup_status_scheduled_city_branches():
    """
    Cutoff calculation:
    is_scheduled=True -> cutoff = 10
    is_airport=False  -> cutoff remains 10
    """
    # on_time (>= 10)
    assert pickup_status(15, True, False) == "on_time"
    assert pickup_status(10, True, False) == "on_time"
    # delayed (>= -5 and < 10)
    assert pickup_status(9, True, False) == "delayed"
    assert pickup_status(-5, True, False) == "delayed"
    # missed (< -5)
    assert pickup_status(-6, True, False) == "missed"


def test_pickup_status_unscheduled_airport_branches():
    """
    Cutoff calculation:
    is_scheduled=False -> cutoff = 5
    is_airport=True    -> cutoff += 10 -> total cutoff = 15
    """
    # on_time (>= 15)
    assert pickup_status(20, False, True) == "on_time"
    assert pickup_status(15, False, True) == "on_time"
    # delayed (>= 0 and < 15)
    assert pickup_status(14, False, True) == "delayed"
    assert pickup_status(0, False, True) == "delayed"
    # missed (< 0)
    assert pickup_status(-1, False, True) == "missed"


def test_pickup_status_unscheduled_city_branches():
    """
    Cutoff calculation:
    is_scheduled=False -> cutoff = 5
    is_airport=False   -> cutoff remains 5
    """
    # on_time (>= 5)
    assert pickup_status(10, False, False) == "on_time"
    assert pickup_status(5, False, False) == "on_time"
    # delayed (>= -10 and < 5)
    assert pickup_status(4, False, False) == "delayed"
    assert pickup_status(-10, False, False) == "delayed"
    # missed (< -10)
    assert pickup_status(-11, False, False) == "missed"
