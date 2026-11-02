# Issues found in `ticket_booking_system.py`

Tools: Pylint 4.1.3, Bandit 1.9.4, Flake8 7.5.0 on Python 3.11.9. Line numbers refer to the **original** file (added in commit `a3df87f`, which the reports in `reports/before/` were run on).

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.37/10, 25 messages | **10.00/10**, 0 messages |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | No issues identified |
| Flake8 | 7 violations | 0 violations (the report file is empty because Flake8 prints nothing when the file is clean) |

Pylint score after each commit: 5.37 → 6.00 (Bandit fixes) → 6.60 (Flake8 fixes) → 10.00 (Pylint fixes) → 10.00 (fixes for issues no tool flagged).

Screenshots of each tool run, before and after, are in [`screenshots/`](screenshots/). They were taken in my clone of `SETAPESU26/L5_45_ticket_booking_system`, so the commit hashes in them come from that clone. The before shots used its original commit, `e4bd01e`.

## Issue table

High and medium severity first. Where several tools report the same problem, all of them are listed.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built from a variable (Bandit B605, **High**) | Security | 58 | `os.system("echo Seating chart exported to: " + filename)` passes `filename` to a shell. A name such as `x.txt & whoami` would make the shell run a second command. It also printed the message out of order when stdout was piped, because the shell writes straight to the console while Python's output is still buffered. | Replaced with `print("Seating chart exported to: " + filename)`. No shell is involved, and the `os` import was no longer needed for it. |
| Weak MD5 hash (Bandit B324, **High**) | Security | 47 | `hashlib.md5` is broken for collisions, so two different ticket codes can be made to produce the same "ticket hash". | Switched to `hashlib.sha256(...).hexdigest()`. |
| `eval()` on a promo expression (Bandit B307, **Medium**; Pylint W0123) | Security | 40–43 | `compute_discounted_price` ran `eval(promo_expr)`, so any Python code passed as a "promo" would execute, e.g. `__import__('os').remove('seating_chart.txt')`. | Changed the parameter to a number, `discount_percent`, checked to be between 0 and 100 (otherwise `ValueError`), and returned `round(base_price * (100 - discount_percent) / 100, 2)`. The caller now passes `20` instead of `"base_price * 0.80"`. The output is still 16.0. |
| Hard-coded secret printed on every run (**not flagged by any tool**) | Security | 70, 79 | `box_office_key = "BOX_OFFICE_SECRET_PASS_2026"` sits in the source and `main()` prints it. Bandit's B105 only matches names like `password`, `token` or `secret`. I checked: the same string assigned to `box_office_token` is flagged, but `box_office_key` is not. | The key is read from the `BOX_OFFICE_KEY` environment variable, and the program prints only whether it is `set` or `not set`. |
| Mutable default argument (Pylint W0102) | Bug | 15, 19 | `order_history=[]` is created once, when the function is defined, so every call that does not pass a list appends to the same hidden list. After three reservations, `reserveSeat.__defaults__[0]` held all three, from unrelated customers. | Default changed to `None`, with `if order_history is None: order_history = []` inside the function. |
| Bare `except: pass` (Bandit B110, Low; Pylint W0702; Flake8 E722) | Bug | 24–27 | Every error was swallowed, so `cancel_seat("ZZ")` (a seat that doesn't exist) looked exactly like a successful cancel. It would also hide unrelated errors and even `KeyboardInterrupt`. | Catch only `KeyError`. The function returns `False` for an unknown seat and `True` on success. |
| Predictable random PIN (Bandit B311, Low) | Security | 51 | `random.randint` uses the Mersenne Twister, whose output can be predicted after enough samples. That is not acceptable for a PIN that protects a booking. | `1000 + secrets.randbelow(9000)`, which gives the same 1000–9999 range from a cryptographically secure source. |
| File opened without `with` or an encoding (Pylint R1732, W1514) | Bug | 55–57 | If `write` raised an exception, the file was never closed. Without an encoding, the platform default is used (cp1252 on Windows). | `with open(filename, "w", encoding="utf-8") as chart_file:`. |
| Demo runs on import (**not flagged**) | Bug | 82 | The bare `main()` call at module level meant `import ticket_booking_system` printed the demo, wrote `seating_chart.txt` and printed the secret. | Wrapped it in `if __name__ == "__main__":`. |
| Seating chart is a raw dict dump (**not flagged**) | Output | 56 | `seating_chart.txt` contained `{'A1': {'tier': 'Standard', ...}}` on one line, which is not a usable chart. | The file now has a header row and one aligned line per seat: seat, tier, price and `Sold`/`Available`. |
| Parameter shadows a global; unused loop variable (Pylint W0621, W0612) | Quality | 61, 63 | `get_theater_summary(theater_seats)` hid the module-level `theater_seats`, and `seat` in the loop was never used. | Renamed the parameter to `seats` and replaced the loop with `sum(1 for details in seats.values() if details["is_sold"])`. |
| Unused import and variables (Flake8 F401, F841; Pylint W0611, W0612) | Quality | 6, 31, 41 | `import math` and `booking_fee = 1.50` were never used. `base_price` was reported as unused because it was only read inside the `eval` string. | Removed `math` and `booking_fee`. `base_price` is now genuinely used by the arithmetic that replaced `eval`. |
| Comparison to `None` with `==` (Flake8 E711; Pylint C0121) | Style | 32 | `== None` calls `__eq__`, which a class can override; identity is the correct check. | `if theater_seats.get(seat_id) is None:`. |
| `if`/`else` that just returns `True` or `False` (Pylint R1703, R1705) | Quality | 34–37 | Four lines to return a boolean that already exists. | `return not theater_seats[seat_id]["is_sold"]`. |
| Function name not snake_case (Pylint C0103) | Style | 15 | `reserveSeat` breaks PEP 8 and is inconsistent with the other functions. | Renamed to `reserve_seat`, including the call in `main()`. |
| Missing docstrings (Pylint C0116) | Style | 15, 23, 30, 40, 46, 50, 54, 61, 69 | None of the nine functions said what it does or returns. | Added a one-line docstring to each, noting return values where they matter (for example, `False` for an unknown seat). |
| `%` formatting on an over-long line (Pylint C0209; Flake8 E501) | Style | 19 | The 82-character line went past PEP 8's 79-character limit and used old-style `%` formatting. | Wrapped it in the Flake8 commit, then turned it into an f-string that fits on one line in the Pylint commit. |
| No newline at end of file (Flake8 W292; Pylint C0304) | Style | 82 | POSIX tools and diffs expect a final newline. | Added one. |

## Commits

| Commit | What it fixes |
|--------|---------------|
| `a3df87f` | Adds the original script and the baseline reports in `reports/before/` |
| `cf939bd` | **Bandit**: B605, B324, B307, B311, B110 |
| `29ce248` | **Flake8**: F401, F841, E711, E501, W292 |
| `515372a` | **Pylint**: W0102, C0103, C0116, C0209, R1703/R1705, R1732/W1514, W0621/W0612 (5.37 → 10.00) |
| `40e9ab7` | Issues no tool reported: the hard-coded secret, the missing `__main__` guard and the raw seating chart |
