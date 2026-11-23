import sys


def read_subscribers(path):
    file = open(path)
    text = file.read()
    file.close()
    return text


def build_report(path):
    text = read_subscribers(path)
    lines = text.strip().split("\n")
    rows = lines[1:]  # drop the header row

    total = 0
    group_names = []
    group_counts = []
    for row in rows:
        fields = row.split(",")
        group = fields[3]
        total = total + 1
        if group in group_names:
            index = group_names.index(group)
            group_counts[index] = group_counts[index] + 1
        else:
            group_names.append(group)
            group_counts.append(1)

    report = "Total: " + str(total)
    i = 0
    while i < len(group_names):
        report = report + "\n" + group_names[i] + ": " + str(group_counts[i])
        i = i + 1
    return report


def main():
    command = sys.argv[1]
    if command == "subscribers":
        print(build_report("data/subscribers.csv"))


if __name__ == "__main__":
    main()
