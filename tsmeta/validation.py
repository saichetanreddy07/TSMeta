"""Generic validation utilities for tabular datasets."""

from dataclasses import dataclass

import pandas as pd


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
    """

    rows: int
    columns: int
    is_empty: bool
    is_valid: bool
    duplicate_rows: int
    missing_values: dict[str, int]
    dtypes: dict[str, str]

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

    is_empty = df.empty
    return ValidationReport(
        rows=len(df),
        columns=len(df.columns),
        is_empty=is_empty,
        is_valid=not is_empty,
        duplicate_rows=int(df.duplicated().sum()),
        missing_values=_missing_value_counts(df),
        dtypes=_column_dtypes(df),
    )


def _missing_value_counts(df: pd.DataFrame) -> dict[str, int]:
    """Return missing-value counts keyed by string column name."""
    return {str(column): int(count) for column, count in df.isna().sum().items()}


def _column_dtypes(df: pd.DataFrame) -> dict[str, str]:
    """Return data type names keyed by string column name."""
    return {str(column): str(dtype) for column, dtype in df.dtypes.items()}
