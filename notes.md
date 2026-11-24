# Notes: my questions and answers

Q: What does `uv run` do that plain `python` does not?

A: `uv run` makes sure your code runs with the exact project setup described in `pyproject.toml` — the right Python version, and all the packages the project needs — before running it. If those packages or the right Python aren't installed yet, `uv run` installs/sets them up automatically first. Plain `python` just uses whatever Python and packages happen to already be active on your computer at that moment, with no check or setup step.

---

Q: What does a classmate get if they clone this repository now?

A: They get exactly what's tracked in git — no virtual environment or lock file, since those aren't committed. So they'd have `main.py` (just a "Hello from mailroom!" placeholder right now), `pyproject.toml` (says the project needs Python 3.12+, no dependencies yet), `.python-version` (pins Python to 3.12), `AGENTS.md` / `CLAUDE.md` (the project rules), `README.md` (empty), and `.gitignore`. Nothing is installed yet. The first thing they'd run is `uv run main.py`, and `uv` would create the `.venv` and set everything up at that point, right there on their machine.

---

Q: Before writing the three functions in mailroom.py, write tests in check.py for: read_subscribers' output type is a string, total emails is 24, and the daily-drinkers group has 8 rows. Each test should check behavior only, not re-implement the counting logic, and should state the expected outcome when it fails.

A: Wrote three tests in `check.py`, importing `read_subscribers`, `count_emails`, and `count_daily_drinkers` from a `mailroom` module that doesn't exist yet. Each test just calls the function and asserts the expected result, with an f-string message naming what was expected and what was actually returned — no row-parsing logic duplicated in the test file. Ran `uv run pytest check.py -v` — it fails at collection with `ModuleNotFoundError: No module named 'mailroom'`, which is expected since `mailroom.py` hasn't been written yet.

---

Q: What is the difference between `uv run python check.py` and `uv run pytest check.py -v`, and why the `-v` flag?

A: `uv run python check.py` hands the file to the plain `python` interpreter, which just executes the file top to bottom. `check.py` only *defines* functions named `test_...` — defining a function doesn't call it — so nothing in the file ever runs, and the silence means "nothing happened," not "it passed." `uv run pytest check.py -v` hands the file to `pytest` instead, which scans it for anything named `test_...`, calls each one itself, and reports pass/fail for each. `-v` means "verbose": without it, pytest prints one dot per passing test (and an `F` per failing one) on a single line; with it, pytest prints each test's full name plus PASSED/FAILED on its own line, which is easier to read while still learning what each check does. The command to trust for "did it actually pass?" is `uv run pytest check.py -v`.

---

Q: Add `subscribers --since-days 30` and `next-send`, both with an optional `--run-date`. OK to use Python's `datetime` module (`date`, `timedelta`) for the date math?

A: Yes, after I explained `date` and `timedelta`: `date` is a calendar date with no time of day; `date.fromisoformat("2026-11-20")` parses one from a string. `timedelta(days=30)` is a span of time, not a date itself — you get the 30-days-ago date by subtracting it from a `date` (`run_date - timedelta(days=30)`), and subtracting two `date`s gives you back a `timedelta`. Every `date` also has `.weekday()`, where Monday is `0` and Sunday is `6`.

---

Q (predicted, then run): `date(2026, 11, 20) - timedelta(days=30)`, `date(2026, 10, 21).weekday()`, `date(2026, 11, 20) <= date(2026, 11, 20)`, `date(2026, 12, 1).weekday()`?

A: `2026-10-21` (crosses the month boundary — subtracting 30 days isn't the same as subtracting 30 from the day digit), `2` (Oct 21, 2026 is a Wednesday), `True` (`<=` includes equal), `1` (Dec 1, 2026 is a Tuesday).

---

Q (predicted, then run): `date(2026, 11, 20).month + 1`, `date(2026, 12, 20).month + 1`, `date(2026, 13, 1)`, and how many days from Dec 1, 2026 (a Tuesday) to the first Monday?

A: `12` and `13` — both are just plain integer math on the `.month` field, not a new date; `date(2026, 13, 1)` raises `ValueError: month must be in 1..12`, which is exactly why `next_send_date` can't just do `month + 1` for December — it has to roll over to January of the next year instead. The answer to the last one is `6` (Dec 1 is Tuesday, `weekday()` 1; Dec 7 is the next day with `weekday()` 0).

---

Q: Why does `next_send_date` start from `date(year, month, 1)` and then check if it's a Monday?

A: Because we want the *first* Monday of next month, we need to start searching from the earliest possible day in that month — day 1 — and then step forward one day at a time (`candidate + timedelta(days=1)`) until `.weekday() == 0`. If the 1st itself is already a Monday, the loop body never runs and day 1 is returned as-is.

---
