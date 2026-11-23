# Mailroom

Mailroom is a command-line tool for one newsletter: Kettlebird Tea's Steep Club.
It reads the subscribers, checks an issue, and sends it to a practice mail server.

- Use uv for everything (`uv add`, `uv run`, `uv sync`, etc.) — never call `pip` or a bare `python` directly.
- Never use a real person's email address. Use `@example.com` for subscriber data, and `@resend.dev` for practice sends.
- Commit and push after every step.
- Behaviors first: I give the expected answers, you write them as checks, show them failing, then write the code.
- Keep `notes.md` updated with every question I ask and the answer, as we go. Separate each question-and-answer pair with `---`.

## How I learn

- I am new to Python. I have completed up to 13.9 of https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/ and I update this number as I learn.
- Write only with what I have learned. If something new would really help, stop and tell me its name in one line. I decide.
- Teach new code using PRIMM-AI+, from https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/you-read-the-agent-writes/. For each new piece of code, run the loop in order:
  1. **Predict** — show me the piece of code. Say nothing about what it does. I write down my guess first.
  2. **Run** — only after I've guessed, run it (with my go-ahead) and show the real output.
  3. **Investigate** — I compare my guess to the output and ask why if they differ. Explain a line only when I ask — never before.
  4. **Modify** — I describe one change; you make that edit. I predict again before you run it again.
  5. **Make** — once I can specify my own version, I describe it, you write it, and I verify it by running it or testing it.
- Nothing is accepted unverified — a run or a test decides, not a claim.
- The loop repeats for the next piece of code.
