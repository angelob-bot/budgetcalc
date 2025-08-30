import importlib.util
import pathlib
import tempfile

import pytest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[2] / "src" / "io" / "csv_io.py"
spec = importlib.util.spec_from_file_location("csv_io", MODULE_PATH)
csv_io = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csv_io)


def test_import_transactions_valid(tmp_path):
    csv_content = """date,description,amount\n2023-01-01,Salary,1000.00\n2023-01-02,Coffee,-3.50\n"""
    file_path = tmp_path / "transactions.csv"
    file_path.write_text(csv_content)
    transactions = csv_io.import_transactions(str(file_path))
    assert transactions == [
        {"date": "2023-01-01", "description": "Salary", "amount": 1000.00},
        {"date": "2023-01-02", "description": "Coffee", "amount": -3.50},
    ]


def test_import_transactions_duplicate(tmp_path):
    csv_content = (
        "date,description,amount\n"
        "2023-01-01,Salary,1000.00\n"
        "2023-01-01,Salary,1000.00\n"
    )
    file_path = tmp_path / "dup.csv"
    file_path.write_text(csv_content)
    with pytest.raises(ValueError):
        csv_io.import_transactions(str(file_path))


def test_import_transactions_parse_error(tmp_path):
    csv_content = (
        "date,description,amount\n"
        "2023-01-01,Salary,notanumber\n"
    )
    file_path = tmp_path / "bad.csv"
    file_path.write_text(csv_content)
    with pytest.raises(ValueError):
        csv_io.import_transactions(str(file_path))


def test_export_transactions_roundtrip(tmp_path):
    transactions = [
        {"date": "2023-01-01", "description": "Salary", "amount": 1000.00},
        {"date": "2023-01-02", "description": "Grocery, Store", "amount": -20.75},
    ]
    file_path = tmp_path / "out.csv"
    csv_io.export_transactions(transactions, str(file_path))
    imported = csv_io.import_transactions(str(file_path))
    assert imported == [
        {"date": "2023-01-01", "description": "Salary", "amount": 1000.0},
        {"date": "2023-01-02", "description": "Grocery, Store", "amount": -20.75},
    ]


def test_export_transactions_duplicate(tmp_path):
    transactions = [
        {"date": "2023-01-01", "description": "Salary", "amount": 1000.00},
        {"date": "2023-01-01", "description": "Salary", "amount": 1000.00},
    ]
    file_path = tmp_path / "dup.csv"
    with pytest.raises(ValueError):
        csv_io.export_transactions(transactions, str(file_path))
