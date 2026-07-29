"""Tests for data cleaning."""

from pathlib import Path

import pandas as pd
import pytest

import tsmeta


def test_clean_data_preserves_input_and_cleans_structure() -> None:
    """Clean structural issues without changing the caller's DataFrame."""
    data = pd.DataFrame(
        {
            " Product Name ": [" A ", " A ", None, None],
            " Value ": ["1", "1", None, None],
            " Empty ": [None, None, None, None],
        }
    )
    original = data.copy(deep=True)

    result = tsmeta.clean_data(data)

    pd.testing.assert_frame_equal(data, original)
    assert list(result.data.columns) == ["product_name", "value"]
    assert result.data.to_dict("records") == [{"product_name": "A", "value": 1}]
    assert result.report.duplicate_rows_removed == 2
    assert result.report.empty_rows_removed == 1
    assert result.report.empty_columns_removed == 1
    assert result.report.column_names_standardized == {
        " Product Name ": "product_name",
        " Value ": "value",
    }
    assert result.report.numeric_columns_converted == ["value"]
    assert result.report.whitespace_trimmed_columns == ["product_name"]


def test_clean_data_converts_datetime_and_fills_missing_values() -> None:
    """Convert date values and fill numeric and categorical missing values."""
    data = pd.DataFrame(
        {
            "Order Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "sales": [1.0, None, 3.0],
            "region": ["north", None, "north"],
        }
    )

    result = tsmeta.clean_data(data)

    assert pd.api.types.is_datetime64_any_dtype(result.data["order_date"])
    assert result.data["sales"].tolist() == [1.0, 2.0, 3.0]
    assert result.data["region"].tolist() == ["north", "north", "north"]
    assert result.report.datetime_columns_converted == ["order_date"]
    assert result.report.numeric_missing_filled == {"sales": 1}
    assert result.report.categorical_missing_filled == {"region": 1}


def test_clean_data_leaves_datetime_missing_values_unchanged() -> None:
    """Do not fill missing values in native datetime columns."""
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", None]),
            "value": [1, 2],
        }
    )

    result = tsmeta.clean_data(data)

    assert pd.isna(result.data.loc[1, "date"])
    assert result.report.numeric_missing_filled == {}
    assert result.report.categorical_missing_filled == {}


def test_clean_data_sorts_single_datetime_column() -> None:
    """Sort a dataset with exactly one datetime column."""
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-03", "2024-01-01", "2024-01-02"]),
            "value": [3, 1, 2],
        }
    )

    result = tsmeta.clean_data(data)

    assert result.data["date"].tolist() == list(
        pd.date_range("2024-01-01", periods=3, freq="D")
    )
    assert result.report.sorted_by_datetime
    assert result.report.missing_timestamps_detected == 0


def test_clean_data_skips_ambiguous_datetime_columns() -> None:
    """Skip time-series processing when datetime column selection is ambiguous."""
    data = pd.DataFrame(
        {
            "start": pd.to_datetime(["2024-01-02", "2024-01-01"]),
            "end": pd.to_datetime(["2024-01-03", "2024-01-02"]),
            "value": [2, 1],
        }
    )

    result = tsmeta.clean_data(data)

    assert result.data["value"].tolist() == [2, 1]
    assert not result.report.sorted_by_datetime


def test_clean_data_inserts_missing_timestamps_and_interpolates() -> None:
    """Insert missing daily timestamps and linearly interpolate numeric values."""
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-03", "2024-01-04"]),
            "value": [1.0, 3.0, 4.0],
        }
    )

    result = tsmeta.clean_data(data, insert_missing_timestamps=True)

    assert result.data["date"].tolist() == list(
        pd.date_range("2024-01-01", periods=4, freq="D")
    )
    assert result.data["value"].tolist() == [1.0, 2.0, 3.0, 4.0]
    assert result.report.missing_timestamps_detected == 1
    assert result.report.missing_timestamps_inserted == 1
    assert result.report.interpolation_method == "linear"


@pytest.mark.parametrize("method, expected", [("ffill", 1.0), ("bfill", 3.0)])
def test_clean_data_supports_fill_interpolation_methods(
    method: str, expected: float
) -> None:
    """Support forward and backward fill for inserted timestamp rows."""
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-03", "2024-01-04"]),
            "value": [1.0, 3.0, 4.0],
        }
    )

    result = tsmeta.clean_data(
        data,
        insert_missing_timestamps=True,
        interpolation_method=method,  # type: ignore[arg-type]
    )

    assert result.data.loc[1, "value"] == expected


def test_cleaning_result_report_methods() -> None:
    """Expose cleaning metadata through summary and dictionary methods."""
    result = tsmeta.clean_data(pd.DataFrame({"value": [1, 1]}))

    assert "Data cleaning summary" in result.summary()
    assert result.to_dict()["report"]["duplicate_rows_removed"] == 1  # type: ignore[index]


@pytest.mark.parametrize("extension", [".csv", ".xlsx"])
def test_cleaning_result_saves_supported_formats(
    tmp_path: Path, extension: str
) -> None:
    """Save cleaned data to every supported file format."""
    result = tsmeta.clean_data(pd.DataFrame({"value": [1, 2]}))
    output_path = tmp_path / f"cleaned{extension}"

    result.save(output_path)

    assert output_path.is_file()


def test_cleaning_result_rejects_unsupported_save_format(tmp_path: Path) -> None:
    """Reject save destinations with unsupported file extensions."""
    result = tsmeta.clean_data(pd.DataFrame({"value": [1]}))

    with pytest.raises(ValueError, match="Unsupported file type"):
        result.save(tmp_path / "cleaned.json")


@pytest.mark.parametrize("invalid_data", [None, [], {"value": [1]}])
def test_clean_data_rejects_invalid_input(invalid_data: object) -> None:
    """Reject inputs that are not pandas DataFrames."""
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        tsmeta.clean_data(invalid_data)


def test_clean_data_rejects_invalid_interpolation_method() -> None:
    """Reject unsupported interpolation methods."""
    with pytest.raises(ValueError, match="interpolation_method"):
        tsmeta.clean_data(
            pd.DataFrame({"value": [1]}),
            interpolation_method="nearest",  # type: ignore[arg-type]
        )
