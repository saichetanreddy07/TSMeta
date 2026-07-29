"""Data cleaning utilities for tabular and time-series datasets."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_object_dtype, is_string_dtype

InterpolationMethod = Literal["linear", "ffill", "bfill"]


@dataclass(frozen=True)
class CleaningReport:
    """Summarize transformations performed during data cleaning.

    Attributes:
        original_rows: Row count before cleaning.
        final_rows: Row count after cleaning.
        original_columns: Column count before cleaning.
        final_columns: Column count after cleaning.
        duplicate_rows_removed: Number of duplicate rows removed.
        empty_rows_removed: Number of fully empty rows removed.
        empty_columns_removed: Number of fully empty columns removed.
        column_names_standardized: Original-to-standardized column name mapping.
        datetime_columns_converted: Columns converted to pandas datetime dtypes.
        numeric_columns_converted: Columns converted to numeric dtypes.
        whitespace_trimmed_columns: String columns whose whitespace was trimmed.
        numeric_missing_filled: Missing numeric values filled, by column.
        categorical_missing_filled: Missing categorical values filled, by column.
        sorted_by_datetime: Whether data was sorted by a single datetime column.
        missing_timestamps_detected: Number of missing timestamps detected.
        missing_timestamps_inserted: Number of missing timestamp rows inserted.
        interpolation_method: Method applied after inserting timestamp rows.
    """

    original_rows: int
    final_rows: int
    original_columns: int
    final_columns: int
    duplicate_rows_removed: int
    empty_rows_removed: int
    empty_columns_removed: int
    column_names_standardized: dict[str, str]
    datetime_columns_converted: list[str]
    numeric_columns_converted: list[str]
    whitespace_trimmed_columns: list[str]
    numeric_missing_filled: dict[str, int]
    categorical_missing_filled: dict[str, int]
    sorted_by_datetime: bool
    missing_timestamps_detected: int
    missing_timestamps_inserted: int
    interpolation_method: InterpolationMethod | None

    def summary(self) -> str:
        """Return a human-readable summary of the cleaning operation.

        Returns:
            A formatted summary of transformations and results.
        """
        return "\n".join(
            [
                "Data cleaning summary",
                f"Rows: {self.original_rows} -> {self.final_rows}",
                f"Columns: {self.original_columns} -> {self.final_columns}",
                f"Duplicate rows removed: {self.duplicate_rows_removed}",
                f"Empty rows removed: {self.empty_rows_removed}",
                f"Empty columns removed: {self.empty_columns_removed}",
                f"Datetime columns converted: {len(self.datetime_columns_converted)}",
                f"Numeric columns converted: {len(self.numeric_columns_converted)}",
                f"Sorted by datetime: {self.sorted_by_datetime}",
                f"Missing timestamps detected: {self.missing_timestamps_detected}",
                f"Missing timestamps inserted: {self.missing_timestamps_inserted}",
                f"Interpolation method: {self.interpolation_method or 'None'}",
            ]
        )

    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary representation of the report.

        Returns:
            A dictionary containing all cleaning report fields.
        """
        return {
            "original_rows": self.original_rows,
            "final_rows": self.final_rows,
            "original_columns": self.original_columns,
            "final_columns": self.final_columns,
            "duplicate_rows_removed": self.duplicate_rows_removed,
            "empty_rows_removed": self.empty_rows_removed,
            "empty_columns_removed": self.empty_columns_removed,
            "column_names_standardized": self.column_names_standardized.copy(),
            "datetime_columns_converted": self.datetime_columns_converted.copy(),
            "numeric_columns_converted": self.numeric_columns_converted.copy(),
            "whitespace_trimmed_columns": self.whitespace_trimmed_columns.copy(),
            "numeric_missing_filled": self.numeric_missing_filled.copy(),
            "categorical_missing_filled": self.categorical_missing_filled.copy(),
            "sorted_by_datetime": self.sorted_by_datetime,
            "missing_timestamps_detected": self.missing_timestamps_detected,
            "missing_timestamps_inserted": self.missing_timestamps_inserted,
            "interpolation_method": self.interpolation_method,
        }


@dataclass(frozen=True)
class CleaningResult:
    """Contain cleaned data and its associated cleaning report."""

    data: pd.DataFrame
    report: CleaningReport

    def summary(self) -> str:
        """Return a human-readable summary of the cleaning operation.

        Returns:
            A formatted cleaning summary.
        """
        return self.report.summary()

    def to_dict(self) -> dict[str, object]:
        """Return a serializable representation of the cleaning result metadata.

        Returns:
            A dictionary containing the cleaning report.
        """
        return {"report": self.report.to_dict()}

    def save(self, path: str | Path) -> None:
        """Save cleaned data to a supported file format.

        Args:
            path: Destination path ending in ``.csv`` or ``.xlsx``.

        Raises:
            ValueError: If the destination file extension is not supported.
        """
        destination = Path(path)
        extension = destination.suffix.lower()
        if extension == ".csv":
            self.data.to_csv(destination, index=False)
            return
        if extension == ".xlsx":
            self.data.to_excel(destination, index=False)
            return
        raise ValueError(
            "Unsupported file type "
            f"'{extension}'. Supported file types are: .csv, .xlsx."
        )


def clean_data(
    df: pd.DataFrame,
    *,
    insert_missing_timestamps: bool = False,
    interpolation_method: InterpolationMethod = "linear",
) -> CleaningResult:
    """Clean a dataset without modifying the input DataFrame.

    Args:
        df: Dataset to clean.
        insert_missing_timestamps: Whether to insert rows for detected timestamps.
        interpolation_method: Method used to fill values in inserted rows.

    Returns:
        The cleaned DataFrame and a report of applied transformations.

    Raises:
        TypeError: If ``df`` is not a pandas DataFrame.
        ValueError: If ``interpolation_method`` is not supported.
    """
    _validate_cleaning_arguments(df, interpolation_method)
    original_rows, original_columns = df.shape
    data = df.copy(deep=True)

    data, structural_details = _clean_structure(data)
    data, type_details = _clean_data_types(data)
    missing_value_details = _fill_missing_values(data)
    data, time_series_details = _clean_time_series(
        data,
        insert_missing_timestamps=insert_missing_timestamps,
        interpolation_method=interpolation_method,
    )

    return CleaningResult(
        data=data,
        report=CleaningReport(
            original_rows=original_rows,
            final_rows=len(data),
            original_columns=original_columns,
            final_columns=len(data.columns),
            duplicate_rows_removed=structural_details.duplicate_rows_removed,
            empty_rows_removed=structural_details.empty_rows_removed,
            empty_columns_removed=structural_details.empty_columns_removed,
            column_names_standardized=structural_details.column_names_standardized,
            datetime_columns_converted=type_details.datetime_columns_converted,
            numeric_columns_converted=type_details.numeric_columns_converted,
            whitespace_trimmed_columns=type_details.whitespace_trimmed_columns,
            numeric_missing_filled=missing_value_details.numeric_missing_filled,
            categorical_missing_filled=missing_value_details.categorical_missing_filled,
            sorted_by_datetime=time_series_details.sorted_by_datetime,
            missing_timestamps_detected=time_series_details.missing_timestamps_detected,
            missing_timestamps_inserted=time_series_details.missing_timestamps_inserted,
            interpolation_method=time_series_details.interpolation_method,
        ),
    )


@dataclass(frozen=True)
class _StructuralDetails:
    """Store transformations from structural cleaning."""

    duplicate_rows_removed: int
    empty_rows_removed: int
    empty_columns_removed: int
    column_names_standardized: dict[str, str]


@dataclass(frozen=True)
class _TypeDetails:
    """Store transformations from data type cleaning."""

    datetime_columns_converted: list[str]
    numeric_columns_converted: list[str]
    whitespace_trimmed_columns: list[str]


@dataclass(frozen=True)
class _MissingValueDetails:
    """Store missing-value replacements by column."""

    numeric_missing_filled: dict[str, int]
    categorical_missing_filled: dict[str, int]


@dataclass(frozen=True)
class _TimeSeriesDetails:
    """Store transformations from time-series cleaning."""

    sorted_by_datetime: bool
    missing_timestamps_detected: int
    missing_timestamps_inserted: int
    interpolation_method: InterpolationMethod | None


def _validate_cleaning_arguments(df: pd.DataFrame, interpolation_method: str) -> None:
    """Validate the public cleaning function arguments."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be a pandas DataFrame; " f"received {type(df).__name__}."
        )
    if interpolation_method not in {"linear", "ffill", "bfill"}:
        raise ValueError("interpolation_method must be one of: linear, ffill, bfill.")


def _clean_structure(df: pd.DataFrame) -> tuple[pd.DataFrame, _StructuralDetails]:
    """Remove structural issues and standardize column names."""
    original_rows, original_columns = df.shape
    data = df.drop_duplicates()
    duplicate_rows_removed = original_rows - len(data)
    data = data.dropna(how="all")
    empty_rows_removed = original_rows - duplicate_rows_removed - len(data)
    data = data.dropna(axis="columns", how="all")
    empty_columns_removed = original_columns - len(data.columns)
    data, column_names_standardized = _standardize_column_names(data)
    return data.reset_index(drop=True), _StructuralDetails(
        duplicate_rows_removed=duplicate_rows_removed,
        empty_rows_removed=empty_rows_removed,
        empty_columns_removed=empty_columns_removed,
        column_names_standardized=column_names_standardized,
    )


def _standardize_column_names(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    """Standardize names by stripping, lowercasing, and replacing whitespace."""
    standardized_names = [
        "_".join(str(column).strip().lower().split()) for column in df
    ]
    changes = {
        str(original): standardized
        for original, standardized in zip(df.columns, standardized_names, strict=True)
        if str(original) != standardized
    }
    data = df.copy()
    data.columns = standardized_names
    return data, changes


def _clean_data_types(df: pd.DataFrame) -> tuple[pd.DataFrame, _TypeDetails]:
    """Convert datetime and numeric data, then trim string whitespace."""
    data, datetime_columns = _convert_datetime_columns(df)
    data, numeric_columns = _convert_numeric_columns(data)
    data, trimmed_columns = _trim_string_whitespace(data)
    return data, _TypeDetails(datetime_columns, numeric_columns, trimmed_columns)


def _convert_datetime_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Convert clearly date-like string columns to pandas datetime dtypes."""
    data = df.copy()
    converted_columns: list[str] = []
    for position, column in enumerate(data.columns):
        series = data.iloc[:, position]
        if not _is_datetime_candidate(column, series):
            continue
        converted = pd.to_datetime(series, errors="coerce")
        if converted.notna().sum() == series.notna().sum():
            data.isetitem(position, converted)
            converted_columns.append(str(column))
    return data, converted_columns


def _is_datetime_candidate(column: object, series: pd.Series) -> bool:
    """Return whether a string column has a date-oriented name and values."""
    if not (is_object_dtype(series) or is_string_dtype(series)):
        return False
    if series.dropna().empty:
        return False
    column_name = str(column).lower()
    return any(token in column_name for token in ("date", "time", "timestamp"))


def _convert_numeric_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Convert fully numeric string columns to numeric dtypes."""
    data = df.copy()
    converted_columns: list[str] = []
    for position, column in enumerate(data.columns):
        series = data.iloc[:, position]
        if not (is_object_dtype(series) or is_string_dtype(series)):
            continue
        non_missing = series.dropna()
        if non_missing.empty:
            continue
        converted = pd.to_numeric(series, errors="coerce")
        if converted.notna().sum() == non_missing.size:
            data.isetitem(position, converted)
            converted_columns.append(str(column))
    return data, converted_columns


def _trim_string_whitespace(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Trim leading and trailing whitespace from string values."""
    data = df.copy()
    trimmed_columns: list[str] = []
    for position, column in enumerate(data.columns):
        series = data.iloc[:, position]
        if not (is_object_dtype(series) or is_string_dtype(series)):
            continue
        trimmed = series.map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
        if not trimmed.equals(series):
            data.iloc[:, position] = trimmed
            trimmed_columns.append(str(column))
    return data, trimmed_columns


def _fill_missing_values(df: pd.DataFrame) -> _MissingValueDetails:
    """Fill numeric and categorical missing values in place."""
    numeric_filled: dict[str, int] = {}
    categorical_filled: dict[str, int] = {}
    for position, column in enumerate(df.columns):
        series = df.iloc[:, position]
        missing_count = int(series.isna().sum())
        if missing_count == 0 or is_datetime64_any_dtype(series):
            continue
        if pd.api.types.is_numeric_dtype(series):
            df.iloc[:, position] = series.fillna(series.mean())
            numeric_filled[str(column)] = missing_count
            continue
        mode = series.mode(dropna=True)
        if not mode.empty:
            df.iloc[:, position] = series.fillna(mode.iloc[0])
            categorical_filled[str(column)] = missing_count
    return _MissingValueDetails(numeric_filled, categorical_filled)


def _clean_time_series(
    df: pd.DataFrame,
    *,
    insert_missing_timestamps: bool,
    interpolation_method: InterpolationMethod,
) -> tuple[pd.DataFrame, _TimeSeriesDetails]:
    """Sort and optionally complete datasets with exactly one datetime column."""
    datetime_positions = [
        position
        for position, dtype in enumerate(df.dtypes)
        if is_datetime64_any_dtype(dtype)
    ]
    if len(datetime_positions) != 1:
        return df, _TimeSeriesDetails(False, 0, 0, None)

    datetime_column = df.columns[datetime_positions[0]]
    data = df.sort_values(datetime_column, kind="stable").reset_index(drop=True)
    missing_timestamps = _missing_timestamps(data[datetime_column])
    if not insert_missing_timestamps or missing_timestamps.empty:
        return data, _TimeSeriesDetails(True, len(missing_timestamps), 0, None)

    if data[datetime_column].duplicated().any():
        return data, _TimeSeriesDetails(True, len(missing_timestamps), 0, None)

    inserted = pd.DataFrame({datetime_column: missing_timestamps})
    data = pd.concat([data, inserted], ignore_index=True)
    data = data.sort_values(datetime_column, kind="stable").reset_index(drop=True)
    _interpolate_inserted_rows(data, datetime_column, interpolation_method)
    return data, _TimeSeriesDetails(
        True,
        len(missing_timestamps),
        len(inserted),
        interpolation_method,
    )


def _missing_timestamps(timestamps: pd.Series) -> pd.DatetimeIndex:
    """Return missing timestamps based on an inferred or regular timedelta frequency."""
    values = timestamps.dropna().drop_duplicates().sort_values()
    if len(values) < 2:
        return pd.DatetimeIndex([])
    frequency = _timestamp_frequency(values)
    if frequency is None:
        return pd.DatetimeIndex([])
    expected = pd.date_range(values.iloc[0], values.iloc[-1], freq=frequency)
    return expected.difference(pd.DatetimeIndex(values))


def _timestamp_frequency(timestamps: pd.Series) -> str | pd.Timedelta | None:
    """Infer a frequency, falling back to a consistent minimum interval."""
    if len(timestamps) >= 3:
        try:
            frequency = pd.infer_freq(timestamps)
        except (TypeError, ValueError):
            frequency = None
        if frequency is not None:
            return frequency

    differences = timestamps.diff().dropna()
    if differences.empty or not (differences > pd.Timedelta(0)).all():
        return None
    minimum_interval = differences.min()
    if (differences % minimum_interval == pd.Timedelta(0)).all():
        return minimum_interval
    return None


def _interpolate_inserted_rows(
    df: pd.DataFrame,
    datetime_column: object,
    interpolation_method: InterpolationMethod,
) -> None:
    """Fill values in inserted timestamp rows using the requested method."""
    data_columns = [column for column in df.columns if column != datetime_column]
    if interpolation_method == "linear":
        numeric_columns = [
            column
            for column in data_columns
            if pd.api.types.is_numeric_dtype(df[column])
        ]
        if numeric_columns:
            df.loc[:, numeric_columns] = df[numeric_columns].interpolate(
                method="linear", limit_direction="both"
            )
        return
    df.loc[:, data_columns] = getattr(df[data_columns], interpolation_method)()
