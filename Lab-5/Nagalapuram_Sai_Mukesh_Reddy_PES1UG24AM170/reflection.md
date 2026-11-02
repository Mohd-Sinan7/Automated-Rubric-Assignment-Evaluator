# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** the Flake8 findings and most of the Pylint style messages. The unused `math` import, the unused `booking_fee`, `== None` → `is None`, the missing final newline, the over-long line and the missing docstrings each needed a change of one or two lines. The report gives the exact line and the fix is obvious, so none of them can change how the program behaves.

**Hardest:** `eval()` in `compute_discounted_price` (Bandit B307). Deleting the `eval` call was not enough, because the function's whole interface was "pass me a Python expression". I had to decide what a promo should be instead (a percentage), change the parameter and its one caller, add a range check so a 150% discount raises `ValueError` instead of producing a negative price, and confirm that the demo still prints the same 16.0.

The **mutable default argument** was also harder to understand than to fix. Changing `[]` to `None` takes one line, but seeing why it is a bug means knowing that default values are evaluated once, when the function is defined. I only really saw it after calling `reserveSeat` a few times and printing `reserveSeat.__defaults__`, which by then contained reservations for three different customers.

The hardest problem of all was one **no tool reported**: the hard-coded `BOX_OFFICE_SECRET_PASS_2026`, which was printed on every run. I only found it by reading the program's output, as the repo README suggests.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes. In the original file, both Flake8 (F841) and Pylint (W0612) said `base_price` was "assigned to but never used". It *was* used, but only inside the string `"base_price * 0.80"` that `eval` ran, and a static tool cannot see into a string that will be executed later. Acting on the warning and deleting the variable would have broken the program with a `NameError`. The warning still pointed at a real problem, though: once I replaced `eval` with normal arithmetic, the variable was genuinely used and the warning went away.

Two Bandit findings depend on context. B324 (MD5) and B311 (`random`) are only real problems if the value protects something. For a ticket hash and a booking PIN it does, so I fixed both. For a non-security checksum, `hashlib.md5(..., usedforsecurity=False)` would be the right answer, and Bandit's message suggests exactly that.

The more important lesson was a **false negative**. Bandit's B105 rule looks for hard-coded passwords by variable *name* (`password`, `token`, `secret`, ...). I tested it: assigning the same string to `box_office_token` is flagged, but `box_office_key` is not. A clean Bandit report does not mean that no secrets are left in the code.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **While coding:** run Flake8 and Pylint in the editor so problems are highlighted as I type, which is when they are cheapest to fix.
- **Before each commit:** use a `pre-commit` hook that runs `flake8`, `pylint --fail-under=9.5` and `bandit -ll` (Medium and High only) on the changed files, so badly formatted or insecure code never reaches a commit.
- **In CI:** run the same three commands in a GitHub Actions job on every pull request, and make `main` require that job to pass before merging. Upload the reports as build artifacts so reviewers can read them without running the tools.
- **Shared configuration:** keep the settings (line length, disabled checks, Bandit skips) in `pyproject.toml` or `setup.cfg`, so every developer and the CI server get the same results. When a finding has to be accepted, suppress it only on that line (`# nosec B311`, with a comment explaining why) instead of switching the check off for the whole project.
- **Existing code:** start by failing the build only on new issues and on Bandit High/Medium, then raise the bar as the old warnings are cleaned up.

Static analysis is not a replacement for tests or code review. Three of the problems in this file (the printed secret, the demo running on import, and the unreadable seating chart) were found by reading the output, not by any tool.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** there is no `eval`, no shell command and no hard-coded secret any more. Ticket hashes use SHA-256 and PINs come from `secrets`. Bandit went from 5 issues (2 High) to none.
- **Correctness:** reservations no longer leak into a shared hidden list. `cancel_seat` returns `False` for a seat that doesn't exist instead of silently pretending to succeed. An invalid discount raises `ValueError` instead of producing a wrong price. The seating chart file is always closed, and the export message now appears in the right order.
- **Reusability:** with the `__main__` guard, other code (or a test) can `import ticket_booking_system` without printing the demo or creating `seating_chart.txt`.
- **Readability:** consistent snake_case names, a docstring on every function, f-strings, and simpler logic (`return not ...is_sold` instead of an `if`/`else`; `sum(...)` instead of a counting loop). The file is now readable by someone who has never seen it.
- **Measured:** Pylint went from 5.37/10 to 10.00/10, Flake8 from 7 violations to 0, and Bandit from 5 issues to 0. The program prints the same results as before (apart from the hash, which is now SHA-256, and the secret, which is no longer shown).
