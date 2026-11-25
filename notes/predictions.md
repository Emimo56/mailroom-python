# Predictions

Prediction: there are 24 subscribers total, in 3 different groups, with 8 subscribers in each group.

---

Prompt: Write a subject-line check for an issue file, against `docs/email-rules.md` rule 1 ("Start with a line `Subject: ...` of 50 characters or fewer"). Here are my six cases and the answer I expect for each, fixed before any test or code exists — once the tests are written to match these, the answers don't change; if a test disagrees with the code later, the code is wrong, not this list.

Two judgment calls the rule itself doesn't spell out, so I'm stating them now rather than leaving them to guess later: the 50-character limit counts only the text after `Subject: `, not the prefix; and an empty subject fails even though 0 is "50 or fewer," because a subject with nothing in it isn't a subject.

1. No `Subject:` line at all — the file starts with `Preview: ...` instead → FAIL: "No Subject line found."
2. A `Subject:` line that exists but isn't the first line (something else, e.g. a blank line, comes before it) → FAIL: "Subject line must be the first line."
3. An empty subject — the line is exactly `Subject: ` with nothing after it → FAIL: "Subject line is empty."
4. A subject of exactly 50 characters — `Subject: Your tea box ships this Monday morning, Steep Club` → PASS.
5. A subject of exactly 51 characters — `Subject: Your tea box ships this Monday morning, Steep Club!` → FAIL: "Subject line is 51 characters (limit 50)."
6. A normal, clearly valid subject — `Subject: The Steep Club opens Monday` (27 characters) → PASS.

---


