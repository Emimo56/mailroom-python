from datetime import date

from mailroom import (
    read_subscribers,
    count_emails,
    count_by_group,
    build_subscribers_report,
    count_recent_subscribers,
    count_subscribers_since,
    next_send_date,
    check_subject,
)

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
    result = count_by_group(text)["daily-drinkers"]
    assert result == 8, f"expected 8 daily-drinkers rows, got {result}"


def test_subscribers_report_shows_total_and_each_group():
    text = read_subscribers(DATA_PATH)
    result = build_subscribers_report(text)
    expected = "Total subscribers: 24\ntea-curious: 8\ngift-buyers: 8\ndaily-drinkers: 8"
    assert result == expected, f"expected:\n{expected}\n\ngot:\n{result}"


def test_recent_subscribers_in_last_30_days_is_7():
    text = read_subscribers(DATA_PATH)
    result = count_recent_subscribers(text, date(2026, 11, 20), 30)
    assert result == 7, f"expected 7 recent subscribers, got {result}"


def test_subscribers_since_2026_10_01_is_12():
    text = read_subscribers(DATA_PATH)
    result = count_subscribers_since(text, date(2026, 10, 1), date(2026, 11, 20))
    assert result == 12, f"expected 12 subscribers since 2026-10-01, got {result}"


def test_next_send_after_2026_11_20_is_first_monday_of_december():
    result = next_send_date(date(2026, 11, 20))
    expected = date(2026, 12, 7)
    assert result == expected, f"expected {expected}, got {result}"


def test_next_send_after_2026_12_07_is_first_monday_of_january():
    result = next_send_date(date(2026, 12, 7))
    expected = date(2027, 1, 4)
    assert result == expected, f"expected {expected}, got {result}"


def test_subject_with_no_problems_has_no_problems():
    issue_text = "Subject: The Steep Club opens Monday\n"
    result = check_subject(issue_text)
    assert result == [], f"expected no problems, got {result}"


def test_subject_at_50_characters_has_no_problems():
    issue_text = "Subject: Your Steep Club box ships on Monday with new teas.\n"
    result = check_subject(issue_text)
    assert result == [], f"expected no problems, got {result}"


def test_subject_at_51_characters_is_too_long():
    issue_text = "Subject: Your Steep Club box ships on Monday with fresh teas\n"
    result = check_subject(issue_text)
    assert result == ["Subject is too long"], f"expected one too-long problem, got {result}"


def test_empty_subject_is_empty():
    issue_text = "Subject: \n"
    result = check_subject(issue_text)
    assert result == ["Subject is empty"], f"expected one empty problem, got {result}"


def test_subject_of_only_spaces_is_empty():
    issue_text = "Subject:     \n"
    result = check_subject(issue_text)
    assert result == ["Subject is empty"], f"expected one empty problem, got {result}"


def test_no_subject_line_at_all_is_missing():
    issue_text = "Preview: Your monthly tea box, chosen by our blenders.\n"
    result = check_subject(issue_text)
    assert result == ["Subject line is missing"], f"expected one missing problem, got {result}"
