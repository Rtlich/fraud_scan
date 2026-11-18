"""Build the anomaly report (data/alerts.csv and a Markdown summary)."""


def build_report(df, alerts, path):
    """Write one line per suspicious transaction and a summary per rule.

    TODO: alerts is {transaction_id: [rule names]}.
    """
    raise NotImplementedError
