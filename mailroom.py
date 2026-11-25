import sys
from datetime import date, timedelta


def read_subscribers(path):
    file = open(path)
    text = file.read()
    file.close()
    return text


def count_by_group(text):
    lines = text.strip().split("\n")
    rows = lines[1:]
    counts = {}
    for row in rows:
        fields = row.split(",")
        group = fields[3]
        if group in counts:
            counts[group] = counts[group] + 1
        else:
            counts[group] = 1
    return counts


def count_emails(text):
    lines = text.strip().split("\n")
    rows = lines[1:]
    count = 0
    for row in rows:
        fields = row.split(",")
        email = fields[2]
        if "@" in email:
            count = count + 1
    return count


def build_subscribers_report(text):
    groups = count_by_group(text)
    total = sum(groups.values())
    lines = [f"Total subscribers: {total}"]
    for group, count in groups.items():
        lines.append(f"{group}: {count}")
    return "\n".join(lines)


def count_recent_subscribers(text, run_date, since_days):
    lines = text.strip().split("\n")
    rows = lines[1:]
    cutoff = run_date - timedelta(days=since_days)
    count = 0
    for row in rows:
        fields = row.split(",")
        joined_on = date.fromisoformat(fields[4])
        if joined_on >= cutoff and joined_on <= run_date:
            count = count + 1
    return count


def count_subscribers_since(text, since_date, run_date):
    lines = text.strip().split("\n")
    rows = lines[1:]
    count = 0
    for row in rows:
        fields = row.split(",")
        joined_on = date.fromisoformat(fields[4])
        if joined_on >= since_date and joined_on <= run_date:
            count = count + 1
    return count


def check_subject(issue_text):
    lines = issue_text.split("\n")

    problems = []
    if len(lines) == 0 or not lines[0].startswith("Subject:"):
        found_elsewhere = False
        for line in lines[1:]:
            if line.startswith("Subject:"):
                found_elsewhere = True
                break
        if found_elsewhere:
            problems.append("Subject line must be the first line.")
        else:
            problems.append("Subject line is missing")
        return problems

    subject_line = lines[0]
    subject = subject_line[len("Subject:"):].strip()
    if subject == "":
        problems.append("Subject is empty")
    elif len(subject) > 50:
        problems.append("Subject is too long")
    return problems


def check_preview(issue_text):
    lines = issue_text.split("\n")
    preview_line = None
    for line in lines:
        if line.startswith("Preview:"):
            preview_line = line
            break

    problems = []
    if preview_line is None:
        problems.append("Preview line is missing")
        return problems

    preview = preview_line[len("Preview:"):].strip()
    if len(preview) > 90:
        problems.append("Preview is too long")
    return problems


def check_greeting(issue_text):
    lines = issue_text.split("\n")
    has_greeting_line = False
    for line in lines:
        if line.startswith("Hi") and "{{first_name}}" in line:
            has_greeting_line = True
            break

    problems = []
    if not has_greeting_line:
        problems.append("Greeting is missing")
    return problems


def split_off_footer(issue_text):
    lines = issue_text.split("\n")
    while len(lines) > 0 and lines[-1].strip() == "":
        lines = lines[:-1]

    if len(lines) < 2:
        return issue_text, False

    disclosure_line = lines[-2]
    unsubscribe_line = lines[-1]
    has_disclosure = disclosure_line.strip() != ""
    has_unsubscribe = (
        "unsubscribe" in unsubscribe_line.lower()
        and "{{unsubscribe_url}}" in unsubscribe_line
    )

    if has_disclosure and has_unsubscribe:
        body_lines = lines[:-2]
        body_text = "\n".join(body_lines)
        return body_text, True

    return issue_text, False


def check_links(issue_text):
    body_text, _ = split_off_footer(issue_text)

    link_count = 0
    i = 0
    while i < len(body_text):
        if body_text[i:i + len("http://")] == "http://":
            link_count = link_count + 1
        elif body_text[i:i + len("https://")] == "https://":
            link_count = link_count + 1
        i = i + 1

    problems = []
    if link_count == 0:
        problems.append("Link is missing")
    elif link_count > 1:
        problems.append("More than one link")
    return problems


def check_footer(issue_text):
    _, has_footer = split_off_footer(issue_text)

    problems = []
    if not has_footer:
        problems.append("Footer is missing")
    return problems


def check_issue(issue_text):
    problems = []
    for problem in check_subject(issue_text):
        problems.append(problem)
    for problem in check_preview(issue_text):
        problems.append(problem)
    for problem in check_greeting(issue_text):
        problems.append(problem)
    for problem in check_links(issue_text):
        problems.append(problem)
    for problem in check_footer(issue_text):
        problems.append(problem)
    return problems


def next_send_date(run_date):
    if run_date.month == 12:
        year = run_date.year + 1
        month = 1
    else:
        year = run_date.year
        month = run_date.month + 1
    candidate = date(year, month, 1)
    while candidate.weekday() != 0:
        candidate = candidate + timedelta(days=1)
    return candidate


if __name__ == "__main__":
    command = sys.argv[1]
    options = sys.argv[2:]

    since_days = None
    since_text = None
    run_date_text = None
    i = 0
    while i < len(options):
        if options[i] == "--since-days":
            since_days = int(options[i + 1])
            i = i + 2
        elif options[i] == "--since":
            since_text = options[i + 1]
            i = i + 2
        elif options[i] == "--run-date":
            run_date_text = options[i + 1]
            i = i + 2
        else:
            i = i + 1

    if run_date_text:
        run_date = date.fromisoformat(run_date_text)
    else:
        run_date = date.today()

    if command == "subscribers":
        text = read_subscribers("data/subscribers.csv")
        if since_text:
            since_date = date.fromisoformat(since_text)
            count = count_subscribers_since(text, since_date, run_date)
            print(f"Subscribers since {since_date}: {count}")
        elif since_days:
            count = count_recent_subscribers(text, run_date, since_days)
            print(f"Subscribers in the last {since_days} days: {count}")
        else:
            print(build_subscribers_report(text))
    elif command == "next-send":
        print(next_send_date(run_date))
    elif command == "check":
        path = options[0]
        file = open(path)
        issue_text = file.read()
        file.close()
        problems = check_issue(issue_text)
        if problems:
            for problem in problems:
                print(problem)
            sys.exit(1)
        else:
            print("OK")
