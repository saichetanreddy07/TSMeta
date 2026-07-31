"""Tests for generic dataset validation."""

import pandas as pd
import pytest

import tsmeta


def test_validate_data_reports_normal_dataframe() -> None:
    """Report generic details for a populated DataFrame."""
    data = pd.DataFrame({"name": ["A", "B"], "value": [1, 2]})

    report = tsmeta.validate_data(data)

    assert isinstance(report, tsmeta.ValidationReport)
    assert report.rows == 2
    assert report.columns == 2
    assert not report.is_empty
    assert report.is_valid
    assert report.duplicate_rows == 0
    assert report.missing_values == {"name": 0, "value": 0}
    assert report.dtypes == {
        str(column): str(dtype) for column, dtype in data.dtypes.items()
    }


def test_validate_data_reports_empty_dataframe() -> None:
    """Mark an empty DataFrame as invalid under the current rule."""
    data = pd.DataFrame(columns=["name", "value"])

    report = tsmeta.validate_data(data)

    assert report.rows == 0
    assert report.columns == 2
    assert report.is_empty
    assert not report.is_valid


def test_validate_data_counts_duplicate_rows() -> None:
    """Count duplicate rows without treating them as invalid yet."""
    data = pd.DataFrame({"name": ["A", "A", "B"], "value": [1, 1, 2]})

    report = tsmeta.validate_data(data)

    assert report.duplicate_rows == 1
    assert report.is_valid


def test_validate_data_counts_missing_values() -> None:
    """Report missing values for each column."""
    data = pd.DataFrame({"name": ["A", None], "value": [None, 2]})

    report = tsmeta.validate_data(data)

    assert report.missing_values == {"name": 1, "value": 1}


@pytest.mark.parametrize("invalid_data", [None, [], {"value": [1]}])
def test_validate_data_rejects_non_dataframe_input(invalid_data: object) -> None:
    """Reject inputs that are not pandas DataFrames."""
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        tsmeta.validate_data(invalid_data)


def test_validation_report_summary_is_human_readable() -> None:
    """Create a concise summary of validation results."""
    report = tsmeta.validate_data(pd.DataFrame({"value": [1, None]}))

    summary = report.summary()

    assert "Dataset validation summary" in summary
    assert "Rows: 2" in summary
    assert "Columns: 1" in summary
    assert "Valid (non-empty dataset): True" in summary
    assert "Missing values: 1" in summary


def test_validation_report_to_dict_is_serializable() -> None:
    """Return all report fields as a dictionary."""
    report = tsmeta.validate_data(pd.DataFrame({"value": [1, None]}))

    result = report.to_dict()

    assert result == {
        "rows": 2,
        "columns": 1,
        "is_empty": False,
        "is_valid": True,
        "duplicate_rows": 0,
        "missing_values": {"value": 1},
        "dtypes": {"value": "float64"},
        "datetime_columns": [],
        "selected_datetime_column": None,
        "duplicate_timestamps": 0,
        "is_sorted": False,
        "inferred_frequency": None,
        "is_univariate": True,
        "is_multivariate": False,
        "is_timeseries": False,
    }

    result["missing_values"]["value"] = 0  # type: ignore[index]
    assert report.missing_values["value"] == 1


def test_validate_data_reports_single_datetime_column() -> None:
    """Identify a single datetime column as the timestamp column."""
    data = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=3, freq="D"),
            "value": [1, 2, 3],
        }
    )

    report = tsmeta.validate_data(data)

    assert report.datetime_columns == ["date"]
    assert report.selected_datetime_column == "date"
    assert report.duplicate_timestamps == 0
    assert report.is_sorted
    assert report.inferred_frequency == "D"
    assert report.is_univariate
    assert not report.is_multivariate
    assert report.is_timeseries


def test_validate_data_reports_no_datetime_column() -> None:
    """Mark datasets without datetime dtypes as non-time-series data."""
    data = pd.DataFrame({"date": ["2024-01-01", "2024-01-02"], "value": [1, 2]})

    report = tsmeta.validate_data(data)

    assert report.datetime_columns == []
    assert report.selected_datetime_column is None
    assert not report.is_timeseries


def test_validate_data_rejects_ambiguous_datetime_columns() -> None:
    """Avoid selecting a timestamp when multiple datetime columns exist."""
    data = pd.DataFrame(
        {
            "start": pd.date_range("2024-01-01", periods=3, freq="D"),
            "end": pd.date_range("2024-01-02", periods=3, freq="D"),
            "value": [1, 2, 3],
        }
    )

    report = tsmeta.validate_data(data)

    assert report.datetime_columns == ["start", "end"]
    assert report.selected_datetime_column is None
    assert not report.is_timeseries


def test_validate_data_reports_duplicate_timestamps() -> None:
    """Count duplicate values in the selected timestamp column."""
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02"]),
            "value": [1, 2, 3],
        }
    )

    report = tsmeta.validate_data(data)

    assert report.duplicate_timestamps == 1
    assert not report.is_timeseries


def test_validate_data_reports_unsorted_timestamps() -> None:
    """Identify timestamps that are not in ascending order."""
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-02", "2024-01-01", "2024-01-03"]),
            "value": [2, 1, 3],
        }
    )

    report = tsmeta.validate_data(data)

    assert not report.is_sorted
    assert not report.is_timeseries


def test_validate_data_reports_irregular_timestamp_frequency() -> None:
    """Return no frequency when timestamp intervals are irregular."""
    data = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-04"]),
            "value": [1, 2, 3],
        }
    )

    report = tsmeta.validate_data(data)

    assert report.inferred_frequency is None
    assert report.is_timeseries


def test_validate_data_identifies_multivariate_dataset() -> None:
    """Identify datasets with multiple non-datetime data columns."""
    data = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=3, freq="D"),
            "sales": [1, 2, 3],
            "returns": [0, 1, 0],
        }
    )

    report = tsmeta.validate_data(data)

    assert not report.is_univariate
    assert report.is_multivariate
