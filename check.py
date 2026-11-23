from mailroom import read_subscribers, count_emails, count_daily_drinkers

DATA_PATH = "data/subscribers.csv"


def test_read_subscribers_returns_a_string():
    result = read_subscribers(DATA_PATH)
    assert isinstance(result, str), f"expected a string, got {type(result).__name__}"


def test_total_number_of_emails_is_24():
    text = read_subscribers(DATA_PATH)
    result = count_emails(text)
    assert result == 24, f"expected 24 emails, got {result}"


def test_daily_drinkers_group_has_8_rows():
    text = read_subscribers(DATA_PATH)
    result = count_daily_drinkers(text)
    assert result == 8, f"expected 8 daily-drinkers rows, got {result}"
