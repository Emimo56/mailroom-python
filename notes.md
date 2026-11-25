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

Q: Would comparing the text `"2026-10-21"` work too? When would it break?

A: It works for this data, because ISO format (`YYYY-MM-DD`, zero-padded) happens to put the digits in the same order as calendar time — `"2026-10-21" <= "2026-11-20"` really is `True`. It breaks without zero-padding (`"2026-9-5" < "2026-10-21"` comes back `False`, since `"9"` sorts after `"1"` character by character) or with a different date format. More importantly, strings can't do date arithmetic — no subtracting 30 days, no `.weekday()` — so `count_recent_subscribers` and `next_send_date` need `date` objects regardless.

---

Q: Add `subscribers --since 2026-10-01`, an exact date instead of a number of days. How many subscribers joined on or after 2026-10-01, as of run date 2026-11-20?

A: 12 — Diego Alvarez, Ana Silva, Grace Okafor, Jonas Berg, Hiroshi Tanaka, Amara Diallo, Noah Fischer, Zainab Hussain, Mateo Rossi, Elif Demir, Yusuf Celik, Kwame Asante. (First guess was 10 — miscounted partway through the sorted list and missed the last two.)

---

Q: Why does Mailroom pass the run date into functions instead of letting each function call `date.today()` itself?

A: This is a CLI tool, and we want to control and run it when we want — passing the run date in means Mailroom can be run against any date we choose (today, a past date, a future date), not only whatever `date.today()` happens to return at the moment it runs.

---

Q: Why is it the test functions that pick the exact dates to pass in, rather than the test calling `date.today()` and checking whatever comes back?

A: Because it keeps the test result the same every time it runs — a fixed run date makes the test deterministic, so it passes the same way today, tomorrow, or a year from now, instead of its expected answer silently changing with the calendar.

---

Q: Explain the error from a hand-typed `2026-02-30` in Jonas Berg's `joined_on` in three lines: what happened, where, why.

A: `date.fromisoformat("2026-02-30")` on line 54 of `count_recent_subscribers` (`mailroom.py`) tried to build a real calendar `date` out of that string. February 2026 only has 28 days, so day 30 doesn't exist for that month. `date.fromisoformat` checks this and raises `ValueError: day is out of range for month` instead of returning a bad or made-up date.

---

Q: Write `check_subject(issue_text)`, which returns a list of problems (empty when the subject is fine), for these cases: "The Steep Club opens Monday" (no problems), a 50-character subject (no problems), a 51-character subject (too long), an empty subject (empty), a subject of only spaces (empty), no Subject line at all (missing).

A: Wrote the six tests first in `test_mailroom.py`, importing `check_subject` from `mailroom` — ran `uv run pytest test_mailroom.py -v` and got an `ImportError: cannot import name 'check_subject'` since the function didn't exist yet. Then wrote `check_subject` in `mailroom.py`: it looks for the first line starting with `"Subject:"`; no such line means `["Subject line is missing"]`; otherwise it takes the text after the colon and strips it — empty after stripping means `["Subject is empty"]` (this covers both a truly empty subject and one of only spaces, since stripping spaces also gives `""`), and longer than 50 characters means `["Subject is too long"]`. All 14 tests pass now, including the 8 that existed before.

---

Q: Check the other rules in `docs/email-rules.md` (preview length, greeting, link count, footer) the same way, with these cases: `issue-01.md` (no problems), a 91-character preview (`"Preview is too long"`), no `{{first_name}}` in the body (`"Greeting is missing"`), two links where even an `http://` one counts (`"More than one link"`), and no footer plus no greeting (`["Greeting is missing", "Footer is missing"]`, in that order). Then add `uv run mailroom.py check <issue file>`, printing every problem on its own line and exiting 1, or printing `OK` and exiting 0.

A: Created four sample issue files under `issues/` (`issue-02-long-preview.md`, `issue-03-no-greeting.md`, `issue-04-two-links.md`, `issue-05-no-greeting-no-footer.md`), then wrote the five tests first in `test_mailroom.py`, importing a new `check_issue` from `mailroom` — ran `uv run pytest test_mailroom.py -v` and got `ImportError: cannot import name 'check_issue'` since it didn't exist yet. Then wrote four small helper functions in `mailroom.py` (`check_preview`, `check_greeting`, `check_links`, `check_footer`) plus `check_issue`, which runs `check_subject` then those four, in that order, and returns the combined list of problems. `check_links` counts `"](http"` in the text, which matches a link written as either `[text](http://...)` or `[text](https://...)`, since both start with `http`; more than one such match is a problem. `check_footer` is one problem (not two) if either the `"You're getting this because"` line or the `"Unsubscribe:"` text is missing. All 19 tests pass. Also added the `check` command to `mailroom.py`'s CLI, which reads the given file, runs `check_issue` on it, prints each problem on its own line and exits 1 if there are any, or prints `OK` and exits 0 otherwise — ran it by hand against `issue-01.md` (`OK`, exit 0) and `issue-05-no-greeting-no-footer.md` (both problems printed, exit 1) to confirm.

---

Q: Test the checks outside the project (temporary broken copies, not committed): a 91-character preview, two links, no footer. Does each one find exactly the right problem?

A: Ran `uv run pytest` (19 passed) and `uv run mailroom.py check issues/issue-01.md` (`OK`). Built three broken copies in a scratch folder outside the project and ran the check on each: the 91-character preview got only `"Preview is too long"`, the two-link copy got only `"More than one link"`, the no-footer copy got only `"Footer is missing"` — each one flagged exactly its own problem, nothing else.

---

Q: Two assumptions `mailroom.py` makes that `docs/email-rules.md` doesn't say anything about: should a missing `Preview:` line be a problem, and should zero links be a problem?

A: Yes to both — a missing Preview line should be flagged, and so should having no link at all. Before this, `check_preview` silently treated "no Preview line" as fine (unlike `check_subject`, which does flag a missing Subject line), and `check_links` only ever checked for *more than* one link, never for zero.

---

Q: Write the two missing-preview and missing-link tests as failing first, then fix the code.

A: Added `test_no_preview_line_at_all_is_missing` (expects `["Preview line is missing"]`) and `test_no_link_at_all_is_missing` (expects `["Link is missing"]`) to `test_mailroom.py` — ran `uv run pytest` and both failed (`check_preview` and `check_links` returned `[]`), while the 19 existing tests still passed. Then fixed `mailroom.py`: `check_preview` now appends `"Preview line is missing"` when there's no Preview line (instead of returning early with no problems), and `check_links` now appends `"Link is missing"` when the link count is `0` (instead of only checking for more than one). All 21 tests pass.

---

Q: `check_links` only counts a link if it sees the literal text `](http` — a Markdown-style link. Should "link" mean specifically that, or any URL-like text in the issue?

A: Any URL in the issue — not just Markdown-style `[text](http...)` links. A bare URL like `https://example.com` with no square brackets should also count.

---

Q: `check_footer` requires the exact phrase `"You're getting this because"` plus the literal text `"Unsubscribe:"`. Should the footer check require that specific wording, or just that some footer-like disclosure and an unsubscribe mention are present, in any wording?

A: Any wording — it just needs some disclosure and some mention of unsubscribing, not that exact phrase.

---

Q: Should a footer/unsubscribe link count toward the "exactly one link" limit, or does "link" mean only links in the body?

A: Body only — a footer/unsubscribe link should not count toward the one-link limit.

---

Q: `check_footer` only checks that the substring `"Unsubscribe:"` appears anywhere in the whole text — not that it contains the literal `{{unsubscribe_url}}` placeholder, and not that the footer is at the end of the file, after the sign-off. Should the check require the placeholder text and the end-of-file position?

A: Yes, require both.

---

Q: How should subject length be counted when the subject contains an emoji like 👍🏽, which is actually two Unicode code points (thumbs up + skin tone modifier) that display as one character?

A: Count length as Python's `len()` counts it — code points, not visible characters. So that emoji counts as 2, not 1.

---
