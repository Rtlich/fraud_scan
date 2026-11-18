"""Run the whole pipeline: python -m fraudscan"""
from fraudscan.loader import load_all


def main():
    df, listings = load_all("data")
    print(f"{len(df)} transactions loaded, {len(listings)} listings")
    # TODO: run the rules, then build the report


if __name__ == "__main__":
    main()
