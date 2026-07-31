"""Tests for dataset analysis."""

import pandas as pd
import pytest

import tsmeta


def test_analyze_reports_normal_dataframe() -> None:
    """Report high-level details for a populated DataFrame."""
    data = pd.DataFrame({"name": ["A", "B"], "value": [1, 2]})

    result = tsmeta.analyze(data)

    assert isinstance(result, tsmeta.AnalysisResult)
    assert isinstance(result.report, tsmeta.DatasetAnalysis)
    assert result.report.rows == 2
    assert result.report.columns == 2
    assert result.report.numeric_columns == 1
    assert result.report.categorical_columns == 1
    assert result.report.datetime_columns == 0
    assert result.report.missing_percentage == 0.0
    assert result.report.duplicate_percentage == 0.0
    assert result.report.memory_usage_bytes == int(data.memory_usage(deep=True).sum())
    assert result.report.memory_usage_mb == result.report.memory_usage_bytes / (1024**2)


def test_analyze_does_not_modify_input_dataframe() -> None:
    """Analyze data without changing the caller's DataFrame."""
    data = pd.DataFrame({"name": [" A ", "B"], "value": [1, None]})
    original = data.copy(deep=True)

    tsmeta.analyze(data)

    pd.testing.assert_frame_equal(data, original)


def test_analyze_reports_empty_dataframe() -> None:
    """Report zero percentages for an empty DataFrame."""
    data = pd.DataFrame(columns=["date", "value"])

    result = tsmeta.analyze(data)

    assert result.report.rows == 0
    assert result.report.columns == 2
    assert result.report.numeric_columns == 0
    assert result.report.categorical_columns == 2
    assert result.report.datetime_columns == 0
    assert result.report.missing_percentage == 0.0
    assert result.report.duplicate_percentage == 0.0


def test_analyze_reports_missing_values() -> None:
    """Calculate missing values as a percentage of all cells."""
    data = pd.DataFrame({"name": ["A", None], "value": [None, 2]})

    result = tsmeta.analyze(data)

    assert result.report.missing_percentage == 50.0


def test_analyze_reports_duplicate_rows() -> None:
    """Calculate duplicate rows as a percentage of all rows."""
    data = pd.DataFrame({"name": ["A", "A", "B", "B"], "value": [1, 1, 2, 3]})

    result = tsmeta.analyze(data)

    assert result.report.duplicate_percentage == 25.0


def test_analyze_reports_multiple_dtypes() -> None:
    """Count numeric, categorical, and datetime columns."""
    data = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=2, freq="D"),
            "sales": [10.0, 12.5],
            "orders": [1, 2],
            "region": pd.Series(["north", "south"], dtype="string"),
            "segment": pd.Series(["retail", "retail"], dtype="category"),
        }
    )

    result = tsmeta.analyze(data)

    assert result.report.numeric_columns == 2
    assert result.report.categorical_columns == 2
    assert result.report.datetime_columns == 1


@pytest.mark.parametrize("invalid_data", [None, [], {"value": [1]}])
def test_analyze_rejects_invalid_input(invalid_data: object) -> None:
    """Reject inputs that are not pandas DataFrames."""
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        tsmeta.analyze(invalid_data)


def test_analysis_result_summary_is_human_readable() -> None:
    """Create a concise summary of analysis results."""
    result = tsmeta.analyze(pd.DataFrame({"value": [1, None]}))

    summary = result.summary()

    assert "Dataset analysis summary" in summary
    assert "Rows: 2" in summary
    assert "Columns: 1" in summary
    assert "Numeric columns: 1" in summary
    assert "Missing values: 50.00%" in summary


def test_analysis_result_to_dict_is_serializable() -> None:
    """Return all analysis fields as a dictionary."""
    data = pd.DataFrame({"value": [1, None]})
    result = tsmeta.analyze(data)

    output = result.to_dict()

    assert output == {
        "report": {
            "rows": 2,
            "columns": 1,
            "numeric_columns": 1,
            "categorical_columns": 0,
            "datetime_columns": 0,
            "missing_percentage": 50.0,
            "duplicate_percentage": 0.0,
            "memory_usage_bytes": int(data.memory_usage(deep=True).sum()),
            "memory_usage_mb": int(data.memory_usage(deep=True).sum()) / (1024**2),
        }
    }
