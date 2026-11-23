from mailroom import read_subscribers

DATA_PATH = "data/subscribers.csv"


def test_read_subscribers_returns_a_string():
    result = read_subscribers(DATA_PATH)
    assert isinstance(result, str)


def test_total_number_of_emails_is_24():
    text = read_subscribers(DATA_PATH)
    lines = text.strip().split("\n")
    rows = lines[1:]  # drop the header row
    count = 0
    for row in rows:
        count = count + 1
    assert count == 24


def test_daily_drinkers_group_has_8_rows():
    text = read_subscribers(DATA_PATH)
    lines = text.strip().split("\n")
    rows = lines[1:]  # drop the header row
    count = 0
    for row in rows:
        fields = row.split(",")
        group = fields[3]
        if group == "daily-drinkers":
            count = count + 1
    assert count == 8
