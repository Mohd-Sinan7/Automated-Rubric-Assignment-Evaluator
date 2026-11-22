# Lab 7: Fuzzing for Input Validation Bugs – Smart Thermostat Controller

**Student:** Rishyendra M (PES1UG24AM154) – Section C, AIML
**Assigned repository:** [SETAPESU26/L6_L7_29_thermostat_control](https://github.com/SETAPESU26/L6_L7_29_thermostat_control) (`lab7/`)

In this repo the handout's `processor.py` / `test_processor.py` are named `thermostat_control.py` / `test_thermostat_control.py`.

## Bugs found by Hypothesis (buggy version: 7 of 9 tests failed)

| Function | Falsifying input (minimised) | Result in buggy code | Root cause |
|----------|------------------------------|----------------------|------------|
| `parse_setpoint` | `None` | `TypeError: 'NoneType' object is not subscriptable` | No type check |
| `parse_setpoint` | `''` | `ValueError: could not convert string to float: ''` | Slices `text[:-1]` with no length check |
| `parse_setpoint` | `'0.0K'` | returns `0.0` | Any unit other than F is silently treated as Celsius |
| `average_temperature` | `None` | `AttributeError: ... no attribute 'split'` | No type check |
| `average_temperature` | `''`, `'20,,21'` | `ValueError: could not convert string to float: ''` | Empty CSV fields not handled |
| `average_temperature` | `'INF'`, `'nan'` | returns `inf` / `nan` | `float()` accepts non-finite values |
| `schedule_slot` | `None` | `AttributeError: ... no attribute 'split'` | No type check |
| `schedule_slot` | `''`, `'0730'` | `ValueError: not enough values to unpack` | Assumes exactly one `:` |
| `schedule_slot` | `':'` | `ValueError: invalid literal for int()` | Empty hour/minute |
| `schedule_slot` | `'0:-1'` | returns `'night -1'` | No range check on hour/minute |
| `schedule_slot` | `'06:00'` | returns `'day 0'` (night returns raw `'00'`) | Inconsistent minute formatting |

## Fixes (defensive programming)

1. Type and length guard on every input (`isinstance(..., str)`, max length → no DoS on huge strings).
2. `parse_setpoint`: strip whitespace, require at least 2 chars and a unit of `C`/`F` only, safe float conversion, reject non-finite and absurd values.
3. `average_temperature`: reject empty fields, convert each part safely, reject `nan`/`inf`, use `math.fsum` and check the result is finite.
4. `schedule_slot`: require exactly one `:`, ASCII digits only, `0 ≤ hour ≤ 23`, `0 ≤ minute ≤ 59`, consistent `MM` format.
5. Invalid input returns `None` and `main()` prints a friendly "Invalid ..." message instead of crashing.

Result: **9/9 Hypothesis tests pass** (500 generated examples per test).

## Contents

| Path | Description |
|------|-------------|
| `PES1UG24AM154_Rishyendra_M_Lab7.pdf` | **Deliverable 1** – PDF document with all screenshots |
| `thermostat_control.py` | **Deliverable 2** – fixed application script |
| `test_thermostat_control.py` | **Deliverable 3** – completed Hypothesis test file |
| `thermostat_control_buggy.py` | Original buggy script (for reference) |
| `reports/` | Raw terminal output of every step |
| `screenshots/` | Step 2: `01a`, `01b` – Step 4: `02a`, `02b` – Step 5: `03` – Step 6: `04` |

## Commands

```
python thermostat_control.py
python -m pytest test_thermostat_control.py
```
