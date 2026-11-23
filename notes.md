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
