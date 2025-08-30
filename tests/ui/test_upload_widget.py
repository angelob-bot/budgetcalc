import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest

from src.ui.upload_widget import UploadWidget


class DummyImportService:
    def __init__(self):
        self.received = []

    def import_file(self, path: str):
        self.received.append(path)


class FailingImportService(DummyImportService):
    def import_file(self, path: str):
        raise ValueError("Malformed file")


def test_accepts_supported_files(tmp_path):
    service = DummyImportService()
    widget = UploadWidget(service)
    file = tmp_path / "data.csv"
    file.write_text("dummy")

    assert widget.drop([str(file)]) is True
    assert service.received == [str(file)]
    assert widget.errors == []


def test_rejects_unsupported_file(tmp_path):
    service = DummyImportService()
    widget = UploadWidget(service)
    file = tmp_path / "data.txt"
    file.write_text("dummy")

    assert widget.drop([str(file)]) is False
    assert service.received == []
    assert "Unsupported file type" in widget.errors[0]


def test_reports_import_errors(tmp_path):
    service = FailingImportService()
    widget = UploadWidget(service)
    file = tmp_path / "data.csv"
    file.write_text("dummy")

    assert widget.drop([str(file)]) is False
    assert "Malformed file" in widget.errors[0]
