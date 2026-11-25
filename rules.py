"""Fraud detection rules.

Each rule takes the clean, joined DataFrame and returns the set of suspicious
transaction_id. The business rules are described in docs/business_rules.md.
"""
import pandas as pd


def refund_without_order(df):
    """Rule 1: a refund whose order_id matches no order."""
    order_ids = set(df.loc[df["type"].eq("order"), "order_id"].dropna())
    refunds = df.loc[df["type"].eq("refund")]
    missing_order_id = refunds["order_id"].isna() | refunds["order_id"].astype(str).str.strip().eq("")
    unmatched_order_id = ~refunds["order_id"].isin(order_ids)
    return set(refunds.loc[missing_order_id | unmatched_order_id, "transaction_id"].dropna())


def repeated_refunds(df):
    """Rule 2: the same buyer refunded at least 3 times within 7 days."""
    refunds = df.loc[
        df["type"].eq("refund")
        & df["buyer_id"].notna()
        & df["datetime"].notna()
    ].copy()
    refunds = refunds.loc[refunds["buyer_id"].astype(str).str.strip().ne("")]
    refunds = refunds.sort_values("datetime")

    flagged = set()
    window = pd.Timedelta(days=7)
    for _, buyer_refunds in refunds.groupby("buyer_id", sort=False):
        transaction_ids = buyer_refunds["transaction_id"].tolist()
        datetimes = buyer_refunds["datetime"].tolist()
        start = 0
        for end, current_datetime in enumerate(datetimes):
            while current_datetime - datetimes[start] > window:
                start += 1
            if end - start + 1 >= 3:
                flagged.update(transaction_ids[start : end + 1])
    return flagged


def new_seller_high_value(df):
    """Rule 3: an order above 300 € by a seller registered less than 7 days ago."""
    raise NotImplementedError


def counterfeit_price(df):
    """Rule 4: a luxury item sold for less than 20 % of its category reference price."""
    raise NotImplementedError


def duplicate_photo(df, listings):
    """Rule 5: an order on a listing whose photo was used earlier by another seller."""
    raise NotImplementedError


def off_platform_contact(df):
    """Rule 6: an order on a listing whose description pushes to contact or pay outside Loopa."""
    raise NotImplementedError


def self_purchase_alias(df):
    """Rule 7: an order where buyer and seller are the same person (same e-mail once the +alias and capitals are ignored)."""
    raise NotImplementedError
