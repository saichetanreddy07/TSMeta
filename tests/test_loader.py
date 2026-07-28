"""Tests for the public data-loading API."""

from pathlib import Path

import pandas as pd
import pytest

import tsmeta
import tsmeta.loader as loader


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Provide a representative tabular dataset."""
    return pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "sales": [10, 15],
        }
    )


def test_load_data_loads_csv(tmp_path: Path, sample_data: pd.DataFrame) -> None:
    """Load data from a CSV file."""
    data_path = tmp_path / "sales.csv"
    sample_data.to_csv(data_path, index=False)

    result = tsmeta.load_data(data_path)

    pd.testing.assert_frame_equal(result, sample_data)


def test_load_data_loads_excel(tmp_path: Path, sample_data: pd.DataFrame) -> None:
    """Load data from an Excel workbook."""
    data_path = tmp_path / "sales.xlsx"
    sample_data.to_excel(data_path, index=False)

    result = tsmeta.load_data(data_path)

    pd.testing.assert_frame_equal(result, sample_data)


def test_load_data_reads_xls_with_excel_reader(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Route legacy Excel files through pandas' Excel reader."""
    data_path = tmp_path / "sales.xls"
    data_path.touch()
    expected = pd.DataFrame({"sales": [10]})

    def read_excel(path: Path) -> pd.DataFrame:
        assert path == data_path
        return expected

    monkeypatch.setattr(loader.pd, "read_excel", read_excel)

    result = tsmeta.load_data(data_path)

    pd.testing.assert_frame_equal(result, expected)


def test_load_data_returns_independent_dataframe(sample_data: pd.DataFrame) -> None:
    """Return a copy when a DataFrame is provided directly."""
    result = tsmeta.load_data(sample_data)
    result.loc[0, "sales"] = 99

    assert result is not sample_data
    assert sample_data.loc[0, "sales"] == 10


def test_load_data_raises_for_missing_file(tmp_path: Path) -> None:
    """Raise a clear error for a missing file."""
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        tsmeta.load_data(missing_path)


def test_load_data_raises_for_unsupported_extension(tmp_path: Path) -> None:
    """Raise a clear error for an unsupported file type."""
    data_path = tmp_path / "sales.json"
    data_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        tsmeta.load_data(data_path)


def test_load_data_raises_for_invalid_source_type() -> None:
    """Raise a clear error for unsupported input objects."""
    with pytest.raises(TypeError, match="source must be"):
        tsmeta.load_data(42)
