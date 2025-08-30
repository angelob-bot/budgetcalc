from pathlib import Path
from typing import Iterable, List


class UploadWidget:
    """Simple widget-like class to handle file drag-and-drop events.

    The widget validates file types and forwards them to an import service
    that implements an ``import_file(path: str)`` method.
    Any errors are collected in ``errors``.
    """

    SUPPORTED_EXTENSIONS = {".csv", ".xls", ".xlsx", ".pdf"}

    def __init__(self, import_service):
        self.import_service = import_service
        self.errors: List[str] = []

    def drop(self, files: Iterable[str]) -> bool:
        """Handle files dropped on the widget.

        Parameters
        ----------
        files:
            Iterable of file paths that were dropped on the widget.

        Returns
        -------
        bool
            ``True`` if all files were handled successfully, ``False`` otherwise.
        """

        self.errors = []
        for file in files:
            path = Path(file)
            ext = path.suffix.lower()
            if ext not in self.SUPPORTED_EXTENSIONS:
                self.errors.append(f"Unsupported file type: {path.name}")
                continue
            try:
                self.import_service.import_file(str(path))
            except Exception as exc:  # pragma: no cover - protects against generic exceptions
                self.errors.append(str(exc))
        return not self.errors

    @property
    def has_errors(self) -> bool:
        """Return ``True`` if the last drop had errors."""
        return bool(self.errors)
