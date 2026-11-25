"""Your tests: for each rule, at least one flagged case and one case that must NOT be flagged."""
import pandas as pd

from fraudscan.rules import refund_without_order, repeated_refunds


def _transaction_frame(rows):
    df = pd.DataFrame(
        rows,
        columns=["transaction_id", "datetime", "type", "order_id", "buyer_id"],
    )
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df


def test_refund_without_order_flags_missing_or_unmatched_order_ids():
    df = _transaction_frame(
        [
            ("T1", "2026-05-01 09:00:00", "order", "O1", "B1"),
            ("T2", "2026-05-01 10:00:00", "refund", "O1", "B1"),
            ("T3", "2026-05-01 11:00:00", "refund", "O2", "B1"),
            ("T4", "2026-05-01 12:00:00", "refund", "", "B1"),
            ("T5", "2026-05-01 13:00:00", "refund", None, "B1"),
            ("T6", "2026-05-01 14:00:00", "order", "O3", "B1"),
        ]
    )

    assert refund_without_order(df) == {"T3", "T4", "T5"}


def test_repeated_refunds_flags_every_refund_in_a_seven_day_window():
    df = _transaction_frame(
        [
            ("T1", "2026-05-01 09:00:00", "refund", "O1", "B1"),
            ("T2", "2026-05-04 09:00:00", "refund", "O2", "B1"),
            ("T3", "2026-05-08 09:00:00", "refund", "O3", "B1"),
            ("T4", "2026-05-01 09:00:00", "refund", "O4", "B2"),
            ("T5", "2026-05-04 09:00:00", "refund", "O5", "B2"),
            ("T6", "2026-05-01 09:00:00", "refund", "O6", "B3"),
            ("T7", "2026-05-09 09:00:00", "refund", "O7", "B3"),
            ("T8", "2026-05-10 09:00:00", "refund", "O8", "B3"),
            ("T9", "2026-05-01 09:00:00", "refund", "O9", None),
            ("T10", "2026-05-02 09:00:00", "refund", "O10", None),
            ("T11", "2026-05-03 09:00:00", "refund", "O11", None),
            ("T12", "2026-05-04 09:00:00", "order", "O12", "B1"),
        ]
    )

    assert repeated_refunds(df) == {"T1", "T2", "T3"}


def test_repeated_refunds_ignores_blank_buyer_ids():
    df = _transaction_frame(
        [
            ("T1", "2026-05-01 09:00:00", "refund", "O1", ""),
            ("T2", "2026-05-02 09:00:00", "refund", "O2", ""),
            ("T3", "2026-05-03 09:00:00", "refund", "O3", ""),
            ("T4", "2026-05-01 09:00:00", "refund", "O4", " "),
            ("T5", "2026-05-02 09:00:00", "refund", "O5", " "),
            ("T6", "2026-05-03 09:00:00", "refund", "O6", " "),
        ]
    )

    assert repeated_refunds(df) == set()
