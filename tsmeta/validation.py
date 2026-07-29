"""Generic validation utilities for tabular datasets."""

from dataclasses import dataclass, field

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype


@dataclass(frozen=True)
class ValidationReport:
    """Summarize generic validation results for a dataset.

    Attributes:
        rows: Number of rows in the dataset.
        columns: Number of columns in the dataset.
        is_empty: Whether the dataset has no data.
        is_valid: Whether the dataset satisfies the current validation rules.
        duplicate_rows: Number of duplicate rows in the dataset.
        missing_values: Missing-value count for each column.
        dtypes: String representation of each column's data type.
        datetime_columns: Names of columns with pandas datetime dtypes.
        selected_datetime_column: The datetime column used for time-series checks.
        duplicate_timestamps: Number of duplicate values in the selected timestamp
            column.
        is_sorted: Whether selected timestamps are in ascending order.
        inferred_frequency: Frequency inferred from selected timestamps, when available.
        is_univariate: Whether the dataset has one non-datetime data column.
        is_multivariate: Whether the dataset has multiple non-datetime data columns.
        is_timeseries: Whether the dataset meets the current time-series rules.
    """

    rows: int
    columns: int
    is_empty: bool
    is_valid: bool
    duplicate_rows: int
    missing_values: dict[str, int]
    dtypes: dict[str, str]
    datetime_columns: list[str] = field(default_factory=list)
    selected_datetime_column: str | None = None
    duplicate_timestamps: int = 0
    is_sorted: bool = False
    inferred_frequency: str | None = None
    is_univariate: bool = False
    is_multivariate: bool = False
    is_timeseries: bool = False

    def summary(self) -> str:
        """Return a human-readable summary of the validation results.

        Returns:
            A formatted validation summary.
        """
        missing_value_count = sum(self.missing_values.values())
        return "\n".join(
            [
                "Dataset validation summary",
                f"Rows: {self.rows}",
                f"Columns: {self.columns}",
                f"Empty: {self.is_empty}",
                f"Valid: {self.is_valid}",
                f"Duplicate rows: {self.duplicate_rows}",
                f"Missing values: {missing_value_count}",
                "Time-series validation",
                f"Datetime columns: {', '.join(self.datetime_columns) or 'None'}",
                f"Selected datetime column: {self.selected_datetime_column or 'None'}",
                f"Duplicate timestamps: {self.duplicate_timestamps}",
                f"Timestamps sorted: {self.is_sorted}",
                f"Inferred frequency: {self.inferred_frequency or 'None'}",
                f"Univariate: {self.is_univariate}",
                f"Multivariate: {self.is_multivariate}",
                f"Time series: {self.is_timeseries}",
            ]
        )

    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary representation of the report.

        Returns:
            A dictionary containing the validation fields.
        """
        return {
            "rows": self.rows,
            "columns": self.columns,
            "is_empty": self.is_empty,
            "is_valid": self.is_valid,
            "duplicate_rows": self.duplicate_rows,
            "missing_values": self.missing_values.copy(),
            "dtypes": self.dtypes.copy(),
            "datetime_columns": self.datetime_columns.copy(),
            "selected_datetime_column": self.selected_datetime_column,
            "duplicate_timestamps": self.duplicate_timestamps,
            "is_sorted": self.is_sorted,
            "inferred_frequency": self.inferred_frequency,
            "is_univariate": self.is_univariate,
            "is_multivariate": self.is_multivariate,
            "is_timeseries": self.is_timeseries,
        }


def validate_data(df: pd.DataFrame) -> ValidationReport:
    """Validate generic properties of a pandas DataFrame.

    Args:
        df: Dataset to validate.

    Returns:
        A report containing generic dataset validation results.

    Raises:
        TypeError: If ``df`` is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be a pandas DataFrame; " f"received {type(df).__name__}."
        )

    datetime_positions = _datetime_column_positions(df)
    datetime_columns = [str(df.columns[position]) for position in datetime_positions]
    time_series_details = _time_series_details(df, datetime_positions)
    return ValidationReport(
        rows=len(df),
        columns=len(df.columns),
        is_empty=df.empty,
        is_valid=not df.empty,
        duplicate_rows=int(df.duplicated().sum()),
        missing_values=_missing_value_counts(df),
        dtypes=_column_dtypes(df),
        datetime_columns=datetime_columns,
        selected_datetime_column=time_series_details.selected_datetime_column,
        duplicate_timestamps=time_series_details.duplicate_timestamps,
        is_sorted=time_series_details.is_sorted,
        inferred_frequency=time_series_details.inferred_frequency,
        is_univariate=time_series_details.is_univariate,
        is_multivariate=time_series_details.is_multivariate,
        is_timeseries=time_series_details.is_timeseries,
    )


def _missing_value_counts(df: pd.DataFrame) -> dict[str, int]:
    """Return missing-value counts keyed by string column name."""
    return {str(column): int(count) for column, count in df.isna().sum().items()}


def _column_dtypes(df: pd.DataFrame) -> dict[str, str]:
    """Return data type names keyed by string column name."""
    return {str(column): str(dtype) for column, dtype in df.dtypes.items()}


def _datetime_column_positions(df: pd.DataFrame) -> list[int]:
    """Return positions of columns with pandas datetime dtypes."""
    return [
        position
        for position, dtype in enumerate(df.dtypes)
        if is_datetime64_any_dtype(dtype)
    ]


@dataclass(frozen=True)
class _TimeSeriesDetails:
    """Store derived time-series validation details."""

    selected_datetime_column: str | None
    duplicate_timestamps: int
    is_sorted: bool
    inferred_frequency: str | None
    is_univariate: bool
    is_multivariate: bool
    is_timeseries: bool


def _time_series_details(
    df: pd.DataFrame, datetime_positions: list[int]
) -> _TimeSeriesDetails:
    """Calculate time-series validation details without modifying the dataset."""
    data_column_count = len(df.columns) - len(datetime_positions)
    is_univariate = data_column_count == 1
    is_multivariate = data_column_count > 1

    if len(datetime_positions) != 1:
        return _TimeSeriesDetails(
            selected_datetime_column=None,
            duplicate_timestamps=0,
            is_sorted=False,
            inferred_frequency=None,
            is_univariate=is_univariate,
            is_multivariate=is_multivariate,
            is_timeseries=False,
        )

    timestamp_column = df.iloc[:, datetime_positions[0]]
    duplicate_timestamps = int(timestamp_column.duplicated().sum())
    is_sorted = timestamp_column.is_monotonic_increasing
    return _TimeSeriesDetails(
        selected_datetime_column=str(timestamp_column.name),
        duplicate_timestamps=duplicate_timestamps,
        is_sorted=is_sorted,
        inferred_frequency=_infer_frequency(timestamp_column),
        is_univariate=is_univariate,
        is_multivariate=is_multivariate,
        is_timeseries=(
            not df.empty
            and data_column_count > 0
            and duplicate_timestamps == 0
            and is_sorted
        ),
    )


def _infer_frequency(timestamps: pd.Series) -> str | None:
    """Infer a timestamp frequency when pandas has sufficient regular data."""
    if len(timestamps) < 3:
        return None

    try:
        return pd.infer_freq(timestamps)
    except (TypeError, ValueError):
        return None
