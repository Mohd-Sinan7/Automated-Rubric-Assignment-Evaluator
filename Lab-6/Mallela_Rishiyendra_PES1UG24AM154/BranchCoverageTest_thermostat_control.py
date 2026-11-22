"""Lab 6 - Branch coverage tests for thermostat_control.py.

Student: Rishyendra M (PES1UG24AM154)
Goal: make every decision (if / or / for) evaluate both True and False,
including boundary values of every comparison (>= 90% branch coverage).
"""
import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert


# ---------------- target_temperature ----------------
@pytest.mark.parametrize("occupied, hour", [(True, 0), (False, 23), (True, 12)])
def test_away_true_branch_ignores_other_inputs(occupied, hour):
    # mode == "away" -> True
    assert target_temperature("away", occupied, hour) == 16


@pytest.mark.parametrize("hour, expected", [
    (0, 18),    # hour < 6 True (short-circuit, second operand not evaluated)
    (5, 18),    # upper boundary of hour < 6
    (6, 20),    # hour < 6 False and hour >= 22 False
    (21, 20),   # just below 22
    (22, 18),   # hour < 6 False, hour >= 22 True
    (23, 18),
])
def test_sleep_mode_all_sub_branches(hour, expected):
    assert target_temperature("sleep", True, hour) == expected


def test_sleep_mode_ignores_occupancy():
    assert target_temperature("sleep", False, 12) == 20


@pytest.mark.parametrize("hour", [0, 7, 18, 23])
def test_not_occupied_true_branch(hour):
    # mode not away/sleep and occupied False -> 18 at any hour
    assert target_temperature("home", False, hour) == 18


@pytest.mark.parametrize("hour, expected", [
    (5, 20),    # 6 <= hour False
    (6, 22),    # morning lower boundary
    (8, 22),    # morning upper boundary
    (9, 20),    # hour < 9 False
    (16, 20),   # 17 <= hour False
    (17, 21),   # evening lower boundary
    (21, 21),   # evening upper boundary
    (22, 20),   # hour < 22 False -> default
])
def test_occupied_time_windows(hour, expected):
    assert target_temperature("home", True, hour) == expected


def test_unknown_mode_treated_as_home():
    assert target_temperature("eco", True, 7) == 22


# ---------------- hvac_action ----------------
@pytest.mark.parametrize("current, target", [(22, 22), (21.1, 22), (22.9, 22)])
def test_idle_true_branch(current, target):
    assert hvac_action(current, target, 15) == "idle"


def test_idle_boundary_diff_exactly_one_heats():
    # abs(diff) < 1 is False when diff == 1
    assert hvac_action(21, 22, 15) == "heat"


def test_idle_boundary_diff_exactly_minus_one_cools():
    assert hvac_action(23, 22, 15) == "cool"


@pytest.mark.parametrize("outside, expected", [
    (-10, "heat_boost"), (4.9, "heat_boost"), (5, "heat"), (20, "heat")])
def test_heating_branches(outside, expected):
    # diff > 0 True, then outside < 5 True / False
    assert hvac_action(15, 22, outside) == expected


@pytest.mark.parametrize("outside, expected", [
    (40, "cool_boost"), (30.1, "cool_boost"), (30, "cool"), (0, "cool")])
def test_cooling_branches(outside, expected):
    # diff > 0 False, then outside > 30 True / False
    assert hvac_action(28, 22, outside) == expected


# ---------------- energy_alert ----------------
def test_empty_readings_loop_not_entered():
    assert energy_alert([], 10) == "ok"


def test_all_readings_under_or_equal_limit_is_ok():
    # loop runs, reading > limit always False (10 == limit is not over)
    assert energy_alert([1, 5, 10], 10) == "ok"


def test_single_reading_over_is_critical():
    assert energy_alert([11], 10) == "critical"


def test_all_readings_over_is_critical():
    assert energy_alert([11, 12, 13, 14], 10) == "critical"


def test_exactly_half_over_is_warning():
    # over * 2 > len(readings) is False when over * 2 == len
    assert energy_alert([11, 12, 1, 2], 10) == "warning"


def test_minority_over_is_warning():
    assert energy_alert([11, 1, 2], 10) == "warning"


def test_majority_over_is_critical():
    assert energy_alert([11, 12, 13, 1, 2], 10) == "critical"
