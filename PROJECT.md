# TSMeta - Project Specification

Version: 0.1.0

Author: Sai Chetan Reddy

---

# Overview

TSMeta is an open-source Python library for loading, validating, cleaning, and
analyzing tabular time-series datasets.

The library is built around pandas DataFrames and provides a simple public API
for common dataset preparation and inspection workflows.

This project specification describes the current v0.1.0 beta implementation.

---

# Core Philosophy

TSMeta should be:

- Modular
- Easy to extend
- Well documented
- Fully typed
- Testable
- Production ready
- Open source friendly

The public API should remain simple even if the internal implementation becomes
more sophisticated.

---

# Target Users

- Data Scientists
- ML Engineers
- AI Engineers
- Business Analysts
- Researchers
- Students
- Python Developers

---

# Public API

The public API is exposed from the `tsmeta` package:

```python
import tsmeta

df = tsmeta.load_data("sales.csv")

validation = tsmeta.validate_data(df)

cleaning = tsmeta.clean_data(df)
cleaned_df = cleaning.data

analysis = tsmeta.analyze(cleaned_df)
```

Current public objects:

- `load_data`
- `validate_data`
- `ValidationReport`
- `clean_data`
- `CleaningResult`
- `CleaningReport`
- `analyze`
- `AnalysisResult`
- `DatasetAnalysis`
- `__version__`

Avoid exposing unnecessary internal helper functions.

---

# Current Modules

`tsmeta/loader.py`

- Loads CSV files.
- Loads Excel files.
- Accepts pandas DataFrames and returns independent copies.
- Raises clear errors for missing files, unsupported file types, and invalid
  input types.

`tsmeta/validation.py`

- Validates generic dataset properties.
- Reports row and column counts, empty state, duplicate rows, missing values,
  and data types.
- Defines `ValidationReport.is_valid` as a non-empty dataset indicator under
  the current validation rules.
- Performs basic time-series validation for datasets with native pandas datetime
  columns.
- Returns a `ValidationReport`.
- Does not modify the input DataFrame.

`tsmeta/cleaning.py`

- Cleans common structural issues.
- Standardizes column names.
- Converts clear datetime and numeric columns.
- Trims string whitespace.
- Fills numeric and categorical missing values.
- Sorts datasets with exactly one datetime column.
- Optionally inserts missing timestamps and fills inserted rows.
- Returns a `CleaningResult` containing cleaned data and cleaning metadata.
- Does not modify the original input DataFrame.

`tsmeta/analysis.py`

- Computes dataset-level statistics.
- Reports row and column counts.
- Counts numeric, categorical, and datetime columns.
- Computes missing value percentage.
- Computes duplicate row percentage.
- Computes memory usage in bytes and MB.
- Returns an `AnalysisResult` containing a `DatasetAnalysis` report.
- Does not modify the input DataFrame.

Each module has one responsibility and should remain independent from the other
pipeline stages.

---

# Architecture

The current pipeline is:

```text
load_data()
    |
    v
validate_data()
    |
    v
clean_data()
    |
    v
analyze()
```

Every stage is independent:

- `load_data()` returns a pandas DataFrame.
- `validate_data()` inspects a DataFrame and returns validation metadata.
- `clean_data()` returns a new cleaned DataFrame and cleaning metadata.
- `analyze()` inspects a DataFrame and returns dataset analysis metadata.

Avoid tightly coupling modules.

---

# Current Scope

- Works with pandas DataFrames.
- Supports CSV and Excel input.
- Performs dataset validation.
- Performs basic time-series validation.
- Cleans datasets without modifying the original input.
- Computes dataset-level statistics.
- Does not modify input data during validation or analysis.
- Assumes at most one datetime column for Version 1 behavior.
- Does not support multiple independent time series.

---

# Coding Standards

Use:

- Python 3.11+
- Type hints everywhere
- Google-style docstrings
- PEP 8
- Ruff compatible formatting and linting
- Black compatible formatting

Maximum function size:

Approximately 50 lines preferred.

Split large functions into smaller reusable helpers.

Avoid duplicated code.

---

# Documentation Rules

Every public function must include:

- Description
- Parameters
- Returns
- Raises
- Example when useful

Example:

```python
def analyze(df):
    """Analyze a dataset without modifying the input DataFrame.

    Args:
        df:
            Input DataFrame.

    Returns:
        AnalysisResult.

    Raises:
        TypeError:
            If the input is not a pandas DataFrame.
    """
```

---

# Error Handling

Never silently ignore errors.

Raise meaningful exceptions.

Examples:

- `FileNotFoundError`
- `ValueError`
- `TypeError`

Provide descriptive messages.

---

# Logging

Never use `print()` inside library code.

Use the standard logging module when logging is necessary.

---

# Testing

Every public feature should include pytest tests.

Tests should cover:

- Normal cases
- Invalid inputs
- Edge cases

---

# Dependencies

Prefer lightweight dependencies.

Avoid introducing unnecessary packages.

Current runtime dependencies:

- pandas
- openpyxl
- xlrd

Current development dependencies:

- black
- pytest
- ruff

Additional dependencies should only be introduced if they provide significant
value.

---

# Performance

Avoid unnecessary loops.

Prefer vectorized pandas operations.

Avoid repeated computations.

Design with scalability in mind.

---

# Versioning

Semantic Versioning:

MAJOR.MINOR.PATCH

Example:

0.1.0

---

# Code Style

Prefer readable code over clever code.

Use meaningful variable names.

Use small reusable functions.

Use consistent naming conventions.

---

# Repository Structure

```text
TSMeta/
  docs/
  examples/
    basic_workflow.py
    cleaning_options.py
    dataframe_input.py
  tests/
  tsmeta/
    __init__.py
    analysis.py
    cleaning.py
    loader.py
    validation.py
  README.md
  CHANGELOG.md
  LICENSE
  pyproject.toml
  PROJECT.md
  ROADMAP.md
```

---

# Current Implementation Status

- `load_data`: CSV, Excel, and DataFrame loading.
- `validate_data`: Generic and time-series dataset validation.
- `clean_data`: Structural, data-type, missing-value, and time-series cleaning.
- `analyze`: Phase 1 dataset-level analysis.

---

# AI Instructions

When generating code:

Always:

- Use type hints.
- Include docstrings.
- Keep functions modular.
- Write production-quality code.
- Generate accompanying tests whenever applicable.

Never sacrifice readability for brevity.

Code should be suitable for an open-source project.
