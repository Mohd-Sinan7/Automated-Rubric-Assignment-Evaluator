# Lab 6: Code and Branch Coverage Analysis – Smart Thermostat Controller

**Student:** Rishyendra M (PES1UG24AM154) – Section C, AIML
**Assigned repository:** [SETAPESU26/L6_L7_29_thermostat_control](https://github.com/SETAPESU26/L6_L7_29_thermostat_control) (`lab6/`)

## Coverage summary (`thermostat_control.py`)

| Phase | Test file | Tests | Line coverage | Branch coverage |
|-------|-----------|-------|---------------|-----------------|
| Starter baseline | `test_thermostat_control.py` | 2 | 26% (9/35 stmts) | 19% (3 partial, 28 branches) |
| Code coverage | `CodeCoverageTest_thermostat_control.py` | 15 | **100%** (35/35) | 100% (28/28) |
| Branch coverage | `BranchCoverageTest_thermostat_control.py` | 43 | **100%** (35/35) | **100%** (28/28, 0 partial) |

## Approach

**Code (line) coverage:** one test per `return` statement – 7 for `target_temperature` (away, sleep-night, sleep-day, unoccupied, morning, evening, default), 5 for `hvac_action` (idle, heat_boost, heat, cool_boost, cool) and 3 for `energy_alert` (ok, critical, warning).

**Branch coverage:** for this module the line tests happen to exercise every branch outcome too, so the branch suite goes further and tests each decision on **both sides of its boundary**, e.g.
- `hour < 6 or hour >= 22`: 0, 5, 6, 21, 22, 23 (covers short-circuit True, second operand True, both False)
- `6 <= hour < 9` and `17 <= hour < 22`: 5, 6, 8, 9, 16, 17, 21, 22
- `abs(diff) < 1`: diff = 0, ±0.9 (idle) and exactly ±1 (not idle)
- `outside < 5` / `outside > 30`: 4.9 / 5 and 30.1 / 30
- `energy_alert` loop: never entered (`[]`), entered with no reading over, reading equal to limit; `over * 2 > len` with exactly half (warning) vs majority (critical)

**Why line coverage can mislead:** a line like `if hour < 6 or hour >= 22: return 18` is fully "covered" by a single test with `hour = 23`, yet the `hour < 6` side of the condition is never exercised. Branch coverage (and boundary values) forces both outcomes of each decision to be tested.

## Contents

| Path | Description |
|------|-------------|
| `thermostat_control.py` | Module under test (unchanged) |
| `test_thermostat_control.py` | Starter tests (baseline) |
| `CodeCoverageTest_thermostat_control.py` | Test cases for code (line) coverage |
| `BranchCoverageTest_thermostat_control.py` | Test cases for branch coverage |
| `reports/` | Raw terminal output of every coverage run |
| `screenshots/` | `00` baseline, `01`–`02` code coverage (line + branch), `03`–`04` branch suite (line + branch), `05` git log |

## Commands

```
python -m coverage run -m pytest CodeCoverageTest_thermostat_control.py
python -m coverage report -m
python -m coverage run --branch -m pytest BranchCoverageTest_thermostat_control.py
python -m coverage report -m
```
