"""Example test: run it with `pytest`."""
from fraudscan.loader import parse_amount


def test_parse_amount_handles_comma_dot_and_missing():
    assert parse_amount("12,50") == 12.5
    assert parse_amount("12.50") == 12.5
    assert parse_amount(" 7 ") == 7.0
    assert parse_amount("") is None
