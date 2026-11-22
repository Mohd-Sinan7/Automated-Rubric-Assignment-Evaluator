"""Lab 6 - Code (line/statement) coverage tests for thermostat_control.py.

Student: Rishyendra M (PES1UG24AM154)
Goal: execute every statement of the module at least once (>= 90% line coverage).
"""
from thermostat_control import target_temperature, hvac_action, energy_alert


# ---------- target_temperature: one test per return statement ----------
def test_away_mode():
    assert target_temperature("away", True, 12) == 16


def test_sleep_mode_night():
    assert target_temperature("sleep", True, 23) == 18


def test_sleep_mode_day():
    assert target_temperature("sleep", True, 12) == 20


def test_home_not_occupied():
    assert target_temperature("home", False, 12) == 18


def test_home_morning():
    assert target_temperature("home", True, 7) == 22


def test_home_evening():
    assert target_temperature("home", True, 18) == 21


def test_home_default():
    assert target_temperature("home", True, 12) == 20


# ---------- hvac_action: one test per return statement ----------
def test_idle_when_close_to_target():
    assert hvac_action(21.5, 22, 15) == "idle"


def test_heat_boost_when_cold_outside():
    assert hvac_action(15, 22, 0) == "heat_boost"


def test_heat_when_mild_outside():
    assert hvac_action(15, 22, 10) == "heat"


def test_cool_boost_when_hot_outside():
    assert hvac_action(28, 22, 35) == "cool_boost"


def test_cool_when_warm_outside():
    assert hvac_action(28, 22, 25) == "cool"


# ---------- energy_alert: one test per return statement ----------
def test_no_readings():
    assert energy_alert([], 10) == "ok"


def test_critical_when_most_readings_over():
    assert energy_alert([12, 15, 11], 10) == "critical"


def test_warning_when_some_readings_over():
    assert energy_alert([5, 6, 12], 10) == "warning"
