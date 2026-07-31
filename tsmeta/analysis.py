"""Dataset analysis utilities for tabular time-series data."""

from dataclasses import dataclass

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype


@dataclass(frozen=True)
class DatasetAnalysis:
    """Summarize high-level dataset characteristics.

    Attributes:
        rows: Number of rows in the dataset.
        columns: Number of columns in the dataset.
        numeric_columns: Number of numeric columns.
        categorical_columns: Number of categorical, string, or object columns.
        datetime_columns: Number of datetime columns.
        missing_percentage: Percentage of missing cells in the dataset.
        duplicate_percentage: Percentage of rows that are duplicates.
        memory_usage_bytes: Total memory usage in bytes.
        memory_usage_mb: Total memory usage in megabytes.
    """

    rows: int
    columns: int
    numeric_columns: int
    categorical_columns: int
    datetime_columns: int
    missing_percentage: float
    duplicate_percentage: float
    memory_usage_bytes: int
    memory_usage_mb: float

    def summary(self) -> str:
        """Return a human-readable summary of the dataset analysis.

        Returns:
            A formatted analysis summary.
        """
        return "\n".join(
            [
                "Dataset analysis summary",
                f"Rows: {self.rows}",
                f"Columns: {self.columns}",
                f"Numeric columns: {self.numeric_columns}",
                f"Categorical columns: {self.categorical_columns}",
                f"Datetime columns: {self.datetime_columns}",
                f"Missing values: {self.missing_percentage:.2f}%",
                f"Duplicate rows: {self.duplicate_percentage:.2f}%",
                f"Memory usage: {self.memory_usage_bytes} bytes",
                f"Memory usage: {self.memory_usage_mb:.2f} MB",
            ]
        )

    def to_dict(self) -> dict[str, int | float]:
        """Return a serializable dictionary representation of the analysis.

        Returns:
            A dictionary containing all dataset analysis fields.
        """
        return {
            "rows": self.rows,
            "columns": self.columns,
            "numeric_columns": self.numeric_columns,
            "categorical_columns": self.categorical_columns,
            "datetime_columns": self.datetime_columns,
            "missing_percentage": self.missing_percentage,
            "duplicate_percentage": self.duplicate_percentage,
            "memory_usage_bytes": self.memory_usage_bytes,
            "memory_usage_mb": self.memory_usage_mb,
        }


@dataclass(frozen=True)
class AnalysisResult:
    """Contain dataset analysis metadata."""

    report: DatasetAnalysis

    def summary(self) -> str:
        """Return a human-readable summary of the analysis result.

        Returns:
            A formatted analysis summary.
        """
        return self.report.summary()

    def to_dict(self) -> dict[str, dict[str, int | float]]:
        """Return a serializable representation of the analysis result.

        Returns:
            A dictionary containing the analysis report.
        """
        return {"report": self.report.to_dict()}


def analyze(df: pd.DataFrame) -> AnalysisResult:
    """Analyze a dataset without modifying the input DataFrame.

    Args:
        df: Dataset to analyze.

    Returns:
        A result containing high-level dataset analysis.

    Raises:
        TypeError: If ``df`` is not a pandas DataFrame.

    Examples:
        >>> import tsmeta
        >>> result = tsmeta.analyze(data)
        >>> result.report.rows
        100
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be a pandas DataFrame; " f"received {type(df).__name__}."
        )

    memory_usage_bytes = _memory_usage_bytes(df)
    return AnalysisResult(
        report=DatasetAnalysis(
            rows=len(df),
            columns=len(df.columns),
            numeric_columns=_numeric_column_count(df),
            categorical_columns=_categorical_column_count(df),
            datetime_columns=_datetime_column_count(df),
            missing_percentage=_missing_percentage(df),
            duplicate_percentage=_duplicate_percentage(df),
            memory_usage_bytes=memory_usage_bytes,
            memory_usage_mb=_bytes_to_megabytes(memory_usage_bytes),
        )
    )


def _numeric_column_count(df: pd.DataFrame) -> int:
    """Return the number of numeric columns."""
    return len(df.select_dtypes(include="number").columns)


def _categorical_column_count(df: pd.DataFrame) -> int:
    """Return the number of categorical, string, or object columns."""
    return len(df.select_dtypes(include=["category", "object", "string"]).columns)


def _datetime_column_count(df: pd.DataFrame) -> int:
    """Return the number of datetime columns."""
    return sum(1 for dtype in df.dtypes if is_datetime64_any_dtype(dtype))


def _missing_percentage(df: pd.DataFrame) -> float:
    """Return the percentage of missing cells in the dataset."""
    total_cells = df.size
    if total_cells == 0:
        return 0.0
    return float(df.isna().sum().sum() / total_cells * 100)


def _duplicate_percentage(df: pd.DataFrame) -> float:
    """Return the percentage of rows that are duplicates."""
    if len(df) == 0:
        return 0.0
    return float(df.duplicated().sum() / len(df) * 100)


def _memory_usage_bytes(df: pd.DataFrame) -> int:
    """Return total DataFrame memory usage in bytes."""
    return int(df.memory_usage(deep=True).sum())


def _bytes_to_megabytes(size_bytes: int) -> float:
    """Convert bytes to megabytes."""
    return size_bytes / (1024**2)
