import csv
from typing import List, Dict, Any

REQUIRED_FIELDS = {"date", "description", "amount"}

def import_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Read transactions from a CSV file.

    Expected header contains ``date``, ``description`` and ``amount``.
    Amount values are parsed as ``float``.

    Duplicate transactions (same date, description and amount) will cause a
    :class:`ValueError` to be raised.  Any parsing problems will also raise a
    :class:`ValueError`.
    """
    transactions: List[Dict[str, Any]] = []
    seen = set()
    try:
        with open(file_path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None or not REQUIRED_FIELDS.issubset(reader.fieldnames):
                missing = REQUIRED_FIELDS.difference(reader.fieldnames or [])
                raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
            for line_no, row in enumerate(reader, start=2):
                try:
                    date = row["date"].strip()
                    description = row["description"].strip()
                    amount = float(row["amount"])
                except (KeyError, AttributeError):
                    raise ValueError(f"Invalid row on line {line_no}")
                except ValueError:
                    raise ValueError(f"Invalid amount on line {line_no}")
                key = (date, description, amount)
                if key in seen:
                    raise ValueError(f"Duplicate transaction found on line {line_no}: {key}")
                seen.add(key)
                transactions.append({"date": date, "description": description, "amount": amount})
    except csv.Error as exc:
        raise ValueError(f"Error reading CSV: {exc}") from exc
    return transactions

def export_transactions(transactions: List[Dict[str, Any]], file_path: str) -> None:
    """Write ``transactions`` to ``file_path`` as CSV.

    ``transactions`` must be an iterable of mappings containing ``date``,
    ``description`` and ``amount``. Duplicate transactions will raise a
    :class:`ValueError`.
    """
    seen = set()
    with open(file_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["date", "description", "amount"])
        writer.writeheader()
        for idx, tx in enumerate(transactions, start=1):
            if not REQUIRED_FIELDS.issubset(tx.keys()):
                missing = REQUIRED_FIELDS.difference(tx.keys())
                raise ValueError(f"Transaction {idx} missing fields: {', '.join(sorted(missing))}")
            try:
                date = str(tx["date"]).strip()
                description = str(tx["description"]).strip()
                amount = float(tx["amount"])
            except (TypeError, ValueError):
                raise ValueError(f"Invalid transaction at index {idx}")
            key = (date, description, amount)
            if key in seen:
                raise ValueError(f"Duplicate transaction at index {idx}: {key}")
            seen.add(key)
            writer.writerow({"date": date, "description": description, "amount": amount})
