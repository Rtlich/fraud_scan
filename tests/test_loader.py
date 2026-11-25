"""Example test: run it with `pytest`."""
import csv

import pandas as pd

from fraudscan.loader import load_all, parse_amount, parse_datetime


def test_parse_amount_handles_comma_dot_and_missing():
    assert parse_amount("12,50") == 12.5
    assert parse_amount("12.50") == 12.5
    assert parse_amount(" 7 ") == 7.0
    assert parse_amount("") is None


def test_parse_datetime_handles_all_export_formats_and_missing():
    expected = parse_datetime("2026-05-04 10:20:00")
    assert parse_datetime("04/05/2026 10:20") == expected
    assert parse_datetime("2026-05-04T10:20:00") == expected
    assert pd.isna(parse_datetime(""))


def _write_csv(path, columns, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)


def test_load_all_normalizes_joins_and_preserves_missing_values(tmp_path):
    _write_csv(
        tmp_path / "transactions.csv",
        [
            "transaction_id",
            "datetime",
            "type",
            "order_id",
            "listing_id",
            "seller_id",
            "buyer_id",
            "amount",
            "payment_method",
            "refund_reason",
        ],
        [
            [
                "T000001", "04/05/2026 10:20", " Order ", "O000001", " l000001 ",
                " u00001 ", "u00002", "12,50", "card", "",
            ],
            [
                "T000002", "2026-05-04T11:00:00", "order", "O000002", "L000002",
                "u00003", "U00004", "12.00", "card", "",
            ],
            ["T000003", "2026-05-04 12:00:00", "order", "", "", "", "", "", "card", ""],
        ],
    )
    _write_csv(
        tmp_path / "listings.csv",
        [
            "listing_id", "seller_id", "created_at", "title", "category_id",
            "brand", "listed_price", "photo_hash", "description",
        ],
        [
            ["L000001", "U00001", "2026-04-20 09:00:00", "Jean", "womenswear", "", "25.00", "photo1", "Description"],
            ["L000002", "U00003", "2026-04-21 09:00:00", "Pull", "womenswear", "", "20.00", "photo2", "Description"],
        ],
    )
    _write_csv(
        tmp_path / "users.csv",
        ["user_id", "signup_date", "country", "email"],
        [
            ["U00001", "2024-01-10", "FR", "Lea.Martin+ventes@example.com"],
            ["U00002", "2024-03-02", "FR", "lea.martin@example.com"],
            ["U00003", "2024-03-03", "FR", "+loopa@example.net"],
            ["U00004", "2024-03-04", "FR", "+autre@example.net"],
        ],
    )
    _write_csv(
        tmp_path / "categories.csv",
        ["category_id", "label", "reference_price", "luxury"],
        [["womenswear", "Womenswear", "22.00", "no"]],
    )

    transactions, _ = load_all(str(tmp_path))
    assert len(transactions) == 3

    aliased_purchase = transactions.set_index("transaction_id").loc["T000001"]
    assert aliased_purchase["datetime"] == parse_datetime("2026-05-04 10:20:00")
    assert aliased_purchase["amount"] == 12.5
    assert aliased_purchase["seller_id"] == "U00001"
    assert aliased_purchase["seller_signup_date"] == pd.Timestamp("2024-01-10")
    assert aliased_purchase["buyer_signup_date"] == pd.Timestamp("2024-03-02")
    assert aliased_purchase["seller_email_key"] == aliased_purchase["buyer_email_key"]
    assert aliased_purchase["reference_price"] == 22.0

    alias_only_purchase = transactions.set_index("transaction_id").loc["T000002"]
    assert pd.isna(alias_only_purchase["seller_email_key"])
    assert pd.isna(alias_only_purchase["buyer_email_key"])

    incomplete_purchase = transactions.set_index("transaction_id").loc["T000003"]
    assert pd.isna(incomplete_purchase["amount"])
    assert pd.isna(incomplete_purchase["listing_id"])
    assert pd.isna(incomplete_purchase["seller_signup_date"])
    assert pd.isna(incomplete_purchase["buyer_signup_date"])
