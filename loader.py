"""Load and clean the Loopa exports, then join them into one DataFrame.

This loader is given partly working, so that you can start with the rules.
It still has gaps, marked TODO: find them with the agent, then fix them
(the reference tests in tests/test_reference.py tell you when it works).
"""
import pandas as pd

# TODO: the export uses a third date format that is not handled yet.
DATE_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]


def parse_amount(value):
    """Convert '12,50', '12.50' or '' to a float (None when missing)."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip().replace(",", ".")
    return float(text) if text else None


def parse_datetime(value):
    """Parse the date formats listed in DATE_FORMATS (NaT when no format matches)."""
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(text, format=fmt)
        except ValueError:
            continue
    return pd.NaT


def load_transactions(path):
    """Read transactions.csv and return a clean DataFrame."""
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["datetime"] = df["datetime"].map(parse_datetime)
    df["amount"] = df["amount"].map(parse_amount).astype(float)
    df["type"] = df["type"].str.strip().str.lower()
    for col in ["order_id", "listing_id", "seller_id", "buyer_id", "refund_reason"]:
        df[col] = df[col].str.strip().replace("", None)
    # TODO: seller_id is sometimes written in lower case (u00012): the joins with users.csv miss these rows.
    return df


def load_listings(path):
    """Read listings.csv (one line per listing, sold or not)."""
    listings = pd.read_csv(path, dtype=str, keep_default_na=False)
    listings["created_at"] = pd.to_datetime(listings["created_at"])
    listings["listed_price"] = listings["listed_price"].astype(float)
    return listings


def load_users(path):
    """Read users.csv (signup date, country and e-mail of every account)."""
    users = pd.read_csv(path, dtype=str)
    users["signup_date"] = pd.to_datetime(users["signup_date"])
    # TODO (rule 7): the same person can hide behind an alias (name+tag@domain) or capital letters.
    return users


def load_categories(path):
    """Read categories.csv (reference price and luxury flag per category)."""
    categories = pd.read_csv(path, dtype=str)
    categories["reference_price"] = categories["reference_price"].astype(float)
    categories["luxury"] = categories["luxury"].eq("yes")
    return categories


def load_all(folder="data"):
    """Return (df, listings): every transaction joined with its listing, seller and category."""
    tx = load_transactions(f"{folder}/transactions.csv")
    listings = load_listings(f"{folder}/listings.csv")
    users = load_users(f"{folder}/users.csv")
    categories = load_categories(f"{folder}/categories.csv")
    df = (tx.merge(listings.drop(columns="seller_id"), on="listing_id", how="left")
            .merge(users[["user_id", "signup_date"]].rename(columns={"user_id": "seller_id", "signup_date": "seller_signup_date"}),
                   on="seller_id", how="left")
            .merge(categories[["category_id", "reference_price", "luxury"]], on="category_id", how="left"))
    # TODO (rule 7): also join the buyer's account, to compare buyer and seller.
    return df, listings
