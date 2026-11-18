"""Compare your rules with the Trust & Safety investigations: python -m fraudscan.evaluate

data/labeled/ is a small export where every transaction was investigated by a person
(data/labeled/investigations.csv). A rule flags anomalies; only an investigation confirms a fraud.
This script counts true positives, false positives and false negatives: you compute precision and recall.
"""
import sys
import pandas as pd
from fraudscan.loader import load_all
from fraudscan import rules

RULES = ["refund_without_order", "repeated_refunds", "new_seller_high_value", "counterfeit_price",
         "duplicate_photo", "off_platform_contact", "self_purchase_alias"]


def main(folder="data/labeled"):
    df, listings = load_all(folder)
    truth = pd.read_csv(f"{folder}/investigations.csv", dtype=str, keep_default_na=False)
    confirmed = set(truth.loc[truth["confirmed_fraud"] == "yes", "transaction_id"])
    notes = dict(zip(truth["transaction_id"], truth["investigation_note"]))
    alerts, done, todo = set(), [], []
    for name in RULES:
        func = getattr(rules, name, None)
        try:
            alerts |= func(df, listings) if name == "duplicate_photo" else func(df)
            done.append(name)
        except NotImplementedError:
            todo.append(name)
    tp, fp, fn = alerts & confirmed, alerts - confirmed, confirmed - alerts
    print(f"Règles évaluées : {', '.join(done) or 'aucune'}")
    print(f"Alertes : {len(alerts)} | fraudes confirmées par enquête : {len(confirmed)}\n")
    print(f"Vrais positifs  (alerte, fraude confirmée)      : {len(tp)}")
    print(f"Faux positifs   (alerte, pas de fraude)         : {len(fp)}")
    print(f"Faux négatifs   (fraude confirmée, sans alerte) : {len(fn)}\n")
    for label, ids in [("Faux positifs", fp), ("Faux négatifs", fn)]:
        for tid in sorted(ids):
            print(f"  {label[:-1]} {tid} : {notes.get(tid) or '(pas de note)'}")
    print("\nÀ vous : précision = VP / (VP + FP) ; rappel = VP / (VP + FN).")


if __name__ == "__main__":
    main(*sys.argv[1:])
