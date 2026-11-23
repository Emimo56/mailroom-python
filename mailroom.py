import sys


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


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "subscribers":
        text = read_subscribers("data/subscribers.csv")
        print(build_subscribers_report(text))
