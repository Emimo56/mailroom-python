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
    check_preview,
    check_greeting,
    check_links,
    check_footer,
    check_issue,
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


def test_subject_not_on_first_line_must_be_first():
    issue_text = "\nSubject: The Steep Club opens Monday\n"
    result = check_subject(issue_text)
    expected = ["Subject line must be the first line."]
    assert result == expected, f"expected {expected}, got {result}"


def test_subject_length_counts_emoji_as_two_characters():
    # "\U0001F44D\U0001F3FD" is one emoji (thumbs up + skin tone) that a
    # person sees as 1 character, but Python's len() counts it as 2.
    # 2 (emoji) + 1 (space) + 48 (rest) = 51 by len() -- over the limit --
    # even though a person counting visible characters would get 50.
    issue_text = "Subject: \U0001F44D\U0001F3FD Thanks so much for joining the Steep Club family\n"
    result = check_subject(issue_text)
    assert result == ["Subject is too long"], f"expected one too-long problem, got {result}"


def test_no_preview_line_at_all_is_missing():
    issue_text = "Subject: The Steep Club opens Monday\n"
    result = check_preview(issue_text)
    assert result == ["Preview line is missing"], f"expected one missing problem, got {result}"


def test_no_link_at_all_is_missing():
    issue_text = "Hi {{first_name}},\n\nNo link here.\n"
    result = check_links(issue_text)
    assert result == ["Link is missing"], f"expected one missing-link problem, got {result}"


def test_bare_url_with_no_brackets_counts_as_a_link():
    issue_text = "Hi {{first_name}},\n\nVisit https://kettlebird.example/steep-club for tea.\n"
    result = check_links(issue_text)
    assert result == [], f"expected no problems, got {result}"


def test_two_bare_urls_is_more_than_one_link():
    issue_text = (
        "Hi {{first_name}},\n\n"
        "Visit https://kettlebird.example/steep-club or https://kettlebird.example/blog.\n"
    )
    result = check_links(issue_text)
    assert result == ["More than one link"], f"expected one too-many-links problem, got {result}"


def test_footer_unsubscribe_link_does_not_count_toward_link_limit():
    issue_text = (
        "Hi {{first_name}},\n\n"
        "[Join The Steep Club](https://kettlebird.example/steep-club)\n\n"
        "Steep well,\n"
        "The Kettlebird Tea team\n\n"
        "You're getting this because you joined the waitlist.\n"
        "Unsubscribe here: https://kettlebird.example/unsub?u={{unsubscribe_url}}\n"
    )
    result = check_links(issue_text)
    assert result == [], f"expected no problems, got {result}"


def test_greeting_placeholder_outside_a_hi_line_is_missing():
    issue_text = (
        "Subject: The Steep Club opens Monday\n"
        "Preview: {{first_name}}, your tea box is here.\n\n"
        "Hi there,\n\n"
        "Welcome to the club.\n"
    )
    result = check_greeting(issue_text)
    assert result == ["Greeting is missing"], f"expected one missing-greeting problem, got {result}"


def test_greeting_on_a_hi_line_has_no_problems():
    issue_text = "Hi {{first_name}},\n\nWelcome to the club.\n"
    result = check_greeting(issue_text)
    assert result == [], f"expected no problems, got {result}"


def test_footer_accepts_any_wording_on_each_line():
    issue_text = (
        "Steep well,\n"
        "The Kettlebird Tea team\n\n"
        "We email you because you signed up for Steep Club updates.\n"
        "Stop these emails: {{unsubscribe_url}}\n"
    )
    result = check_footer(issue_text)
    assert result == [], f"expected no problems, got {result}"


def test_footer_without_the_unsubscribe_placeholder_is_missing():
    issue_text = (
        "Steep well,\n"
        "The Kettlebird Tea team\n\n"
        "You're getting this because you joined the waitlist.\n"
        "Unsubscribe: https://kettlebird.example/unsub\n"
    )
    result = check_footer(issue_text)
    assert result == ["Footer is missing"], f"expected one missing problem, got {result}"


def test_footer_not_at_the_end_of_file_is_missing():
    issue_text = (
        "You're getting this because you joined the waitlist.\n"
        "Unsubscribe: {{unsubscribe_url}}\n\n"
        "P.S. Tell a friend!\n"
    )
    result = check_footer(issue_text)
    assert result == ["Footer is missing"], f"expected one missing problem, got {result}"


def read_issue(path):
    file = open(path)
    text = file.read()
    file.close()
    return text


def test_issue_01_has_no_problems():
    issue_text = read_issue("issues/issue-01.md")
    result = check_issue(issue_text)
    assert result == [], f"expected no problems, got {result}"


def test_issue_with_91_character_preview_is_too_long():
    issue_text = read_issue("issues/issue-02-long-preview.md")
    result = check_issue(issue_text)
    assert result == ["Preview is too long"], f"expected one too-long problem, got {result}"


def test_issue_without_first_name_greeting_is_missing():
    issue_text = read_issue("issues/issue-03-no-greeting.md")
    result = check_issue(issue_text)
    assert result == ["Greeting is missing"], f"expected one missing-greeting problem, got {result}"


def test_issue_with_two_links_has_more_than_one_link():
    issue_text = read_issue("issues/issue-04-two-links.md")
    result = check_issue(issue_text)
    assert result == ["More than one link"], f"expected one too-many-links problem, got {result}"


def test_issue_without_greeting_or_footer_has_two_problems():
    issue_text = read_issue("issues/issue-05-no-greeting-no-footer.md")
    result = check_issue(issue_text)
    expected = ["Greeting is missing", "Footer is missing"]
    assert result == expected, f"expected {expected}, got {result}"
