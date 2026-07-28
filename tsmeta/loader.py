"""Utilities for loading tabular time-series data."""

from pathlib import Path

import pandas as pd

_SUPPORTED_EXTENSIONS = {".csv", ".xls", ".xlsx"}


def load_data(source: str | Path | pd.DataFrame) -> pd.DataFrame:
    """Load tabular data from a supported file or DataFrame.

    Args:
        source: A CSV or Excel file path, or an existing pandas DataFrame.

    Returns:
        A copy of the loaded or provided DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file extension is not supported.
        TypeError: If ``source`` is not a string, Path, or pandas DataFrame.

    Examples:
        >>> import tsmeta
        >>> data = tsmeta.load_data("sales.csv")
    """
    if isinstance(source, pd.DataFrame):
        return source.copy()

    if not isinstance(source, (str, Path)):
        raise TypeError(
            "source must be a str, pathlib.Path, or pandas DataFrame; "
            f"received {type(source).__name__}."
        )

    return _load_file(Path(source).expanduser())


def _load_file(path: Path) -> pd.DataFrame:
    """Load a DataFrame from a supported file path."""
    if not path.is_file():
        raise FileNotFoundError(f"Data file does not exist: {path}")

    extension = path.suffix.lower()
    if extension not in _SUPPORTED_EXTENSIONS:
        supported_extensions = ", ".join(sorted(_SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported file type '{extension}'. "
            f"Supported file types are: {supported_extensions}."
        )

    if extension == ".csv":
        return pd.read_csv(path)

    return pd.read_excel(path)
