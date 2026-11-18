"""Fraud detection rules.

Each rule takes the clean, joined DataFrame and returns the set of suspicious
transaction_id. The business rules are described in docs/business_rules.md.
"""


def refund_without_order(df):
    """Rule 1: a refund whose order_id matches no order."""
    raise NotImplementedError


def repeated_refunds(df):
    """Rule 2: the same buyer refunded at least 3 times within 7 days."""
    raise NotImplementedError


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
