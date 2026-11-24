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
    subject_line = None
    for line in lines:
        if line.startswith("Subject:"):
            subject_line = line
            break

    problems = []
    if subject_line is None:
        problems.append("Subject line is missing")
        return problems

    subject = subject_line[len("Subject:"):].strip()
    if subject == "":
        problems.append("Subject is empty")
    elif len(subject) > 50:
        problems.append("Subject is too long")
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
