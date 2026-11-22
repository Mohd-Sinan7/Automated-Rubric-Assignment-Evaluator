# Lab 5 – Reflection

**Student:** Rishyendra M (PES1UG24AM154)

**1. Which issues were the easiest to fix, and which were the hardest? Why?**
The Flake8 issues (E261, E225, E231, E305) and the Pylint naming/docstring issues were the easiest – they are mechanical and the tool says exactly what to change. The hardest were the security issues from Bandit. Removing the hardcoded PIN and gateway key needed a design decision (environment variables and storing only a hash of the PIN) while keeping the demo working, and the SHA-1 fix also meant changing how the PIN is compared (`hmac.compare_digest`). The `global` warning also needed a small redesign (keeping the limit inside the `wallet` dict).

**2. Did the static analysis tools report any false positives? If so, describe one example.**
Partly. Bandit B105 flagged `GATEWAY_SECRET = "sk_demo_wallet_0000"` as a hardcoded password with only *Low* severity / *Medium* confidence – for a classroom demo the value is clearly a dummy key, so in context it is close to a false positive. Bandit B311 (`random` for the OTP) would also be a false positive if the random number were used for, e.g., a game, because the rule only looks at the function name, not how the value is used. I still fixed both because in a real wallet they would be genuine vulnerabilities.

**3. How would you integrate static analysis tools into your actual software development workflow?**
I would run Flake8 and Pylint automatically through a pre-commit hook so style problems never reach the repository, and run Pylint (with a minimum score such as 9.5), Flake8 and Bandit in a CI pipeline (e.g. GitHub Actions) on every push and pull request, failing the build on any Bandit High/Medium issue. The editor (VS Code) can also show Pylint/Flake8 warnings live while coding.

**4. What tangible improvements did you observe in the code quality, readability, and potential robustness after applying the fixes?**
Pylint went from 5.69/10 to 10.00/10, and Bandit and Flake8 both report zero issues. The code is now consistent (snake_case, docstrings, PEP 8 spacing) and easier to read. Robustness improved: the mutable default bug that shared the `log` list between calls is gone, there is no global state rebinding, the program no longer runs on import, PINs use SHA-256 with constant-time comparison, OTPs come from a cryptographically secure generator, and temp files are created safely – all while producing the same output as before.
