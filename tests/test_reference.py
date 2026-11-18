"""Reference tests from the Loopa Trust & Safety team.

DO NOT MODIFY THIS FILE: it is checked with `git diff` when your work is graded.
They fail until the loader and rules 1 and 2 are written correctly.
Add your own tests in tests/test_rules.py.
"""
from fraudscan.loader import parse_datetime, load_all
from fraudscan import rules


def test_reference_three_date_formats():
    expected = parse_datetime("2026-05-04 10:20:00")
    assert parse_datetime("04/05/2026 10:20") == expected
    assert parse_datetime("2026-05-04T10:20:00") == expected


def test_reference_rule_1_refund_without_order():
    df, _ = load_all("data/sample")
    assert rules.refund_without_order(df) == {"T000012", "T000013"}


def test_reference_rule_2_repeated_refunds():
    df, _ = load_all("data/sample")
    assert rules.repeated_refunds(df) == {"T000014", "T000015", "T000016"}
