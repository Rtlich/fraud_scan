"""Load and clean the Loopa exports, then join them for fraud detection."""
import pandas as pd

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%d/%m/%Y %H:%M",
]


def _normalize_identifier(value):
    """Trim an identifier and normalize its case, keeping missing values absent."""
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return text.upper() if text else None


def _normalize_email(email):
    """Return a case-insensitive email identity without its optional +alias."""
    if email is None or pd.isna(email):
        return None
    text = str(email).strip().casefold()
    local, separator, domain = text.partition("@")
    if not separator or not domain:
        return None
    local = local.partition("+")[0]
    return f"{local}@{domain}" if local else None


def parse_amount(value):
    """Convert '12,50', '12.50' or '' to a float (None when missing)."""
    if value is None or pd.isna(value):
        return None
    text = str(value).strip().replace(",", ".")
    return float(text) if text else None


def parse_datetime(value):
    """Parse the date formats listed in DATE_FORMATS (NaT when no format matches)."""
    if value is None or pd.isna(value):
        return pd.NaT
    text = str(value).strip()
    if not text:
        return pd.NaT
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
    for col in ["order_id", "listing_id", "seller_id", "buyer_id"]:
        df[col] = df[col].map(_normalize_identifier)
    return df


def load_listings(path):
    """Read listings.csv (one line per listing, sold or not)."""
    listings = pd.read_csv(path, dtype=str, keep_default_na=False)
    for col in ["listing_id", "seller_id"]:
        listings[col] = listings[col].map(_normalize_identifier)
    listings["category_id"] = listings["category_id"].str.strip().str.lower()
    listings["created_at"] = pd.to_datetime(listings["created_at"])
    listings["listed_price"] = listings["listed_price"].astype(float)
    return listings


def load_users(path):
    """Read users.csv (signup date, country and e-mail of every account)."""
    users = pd.read_csv(path, dtype=str, keep_default_na=False)
    users["user_id"] = users["user_id"].map(_normalize_identifier)
    users["signup_date"] = pd.to_datetime(users["signup_date"])
    users["email_key"] = users["email"].map(_normalize_email)
    return users


def load_categories(path):
    """Read categories.csv (reference price and luxury flag per category)."""
    categories = pd.read_csv(path, dtype=str, keep_default_na=False)
    categories["category_id"] = categories["category_id"].str.strip().str.lower()
    categories["reference_price"] = categories["reference_price"].astype(float)
    categories["luxury"] = categories["luxury"].str.strip().str.lower().eq("yes")
    return categories


def load_all(folder="data"):
    """Return transactions enriched with listing, seller, buyer, and category data."""
    tx = load_transactions(f"{folder}/transactions.csv")
    listings = load_listings(f"{folder}/listings.csv")
    users = load_users(f"{folder}/users.csv")
    categories = load_categories(f"{folder}/categories.csv")

    seller_users = users[["user_id", "signup_date", "email_key"]].rename(
        columns={
            "user_id": "seller_id",
            "signup_date": "seller_signup_date",
            "email_key": "seller_email_key",
        }
    )
    buyer_users = users[["user_id", "signup_date", "email_key"]].rename(
        columns={
            "user_id": "buyer_id",
            "signup_date": "buyer_signup_date",
            "email_key": "buyer_email_key",
        }
    )
    df = (tx.merge(listings.drop(columns="seller_id"), on="listing_id", how="left")
            .merge(seller_users, on="seller_id", how="left")
            .merge(buyer_users, on="buyer_id", how="left")
            .merge(categories[["category_id", "reference_price", "luxury"]], on="category_id", how="left"))
    return df, listings
