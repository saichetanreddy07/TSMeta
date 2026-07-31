# TSMeta

TSMeta is an open-source Python library for loading, validating, cleaning, and
analyzing tabular time-series datasets.

The project provides a simple public API around pandas DataFrames while keeping
each processing stage independent and easy to test.

## Status

TSMeta currently provides data loading, generic and time-series validation, data
cleaning, and Phase 1 dataset analysis.

## Current Workflow

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

Each stage is independent. Loading returns a DataFrame, validation and analysis
inspect data without modifying it, and cleaning returns a new cleaned DataFrame
with cleaning metadata.

## Installation

TSMeta requires Python 3.11 or later.

```bash
python -m pip install -e .
```

For development tools:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

```python
import tsmeta

df = tsmeta.load_data("sales.csv")

validation = tsmeta.validate_data(df)
print(validation.summary())

cleaning = tsmeta.clean_data(df)
cleaned_df = cleaning.data

analysis = tsmeta.analyze(cleaned_df)
print(analysis.summary())
```

## Features

### Loader

- Load CSV files.
- Load Excel files (`.xlsx` and `.xls`).
- Load pandas DataFrames by returning an independent copy.

### Validation

- Dataset validation for shape, empty data, duplicate rows, missing values, and
  data types.
- Time-series validation for native pandas datetime columns, duplicate
  timestamps, timestamp ordering, inferred frequency, and univariate or
  multivariate structure.
- `ValidationReport` with `summary()` and `to_dict()` methods.

### Cleaning

- Structural cleaning for duplicate rows, empty rows, empty columns, column name
  standardization, and index reset.
- Data type cleaning for datetime conversion, numeric conversion, and string
  whitespace trimming.
- Missing value handling for numeric and categorical columns.
- Time-series cleaning for datasets with exactly one datetime column.
- `CleaningResult` with cleaned data, cleaning metadata, `summary()`,
  `to_dict()`, and `save()` support for CSV and Excel output.

### Analysis

- Dataset statistics.
- Row and column counts.
- Numeric, categorical, and datetime column counts.
- Missing value percentage.
- Duplicate row percentage.
- Memory usage in bytes and MB.
- `AnalysisResult` and `DatasetAnalysis`.

## Usage

### load_data()

```python
import tsmeta

df = tsmeta.load_data("sales.csv")
```

`load_data()` accepts `.csv`, `.xlsx`, `.xls`, `pathlib.Path`, and existing
`pandas.DataFrame` inputs. DataFrame inputs are copied before being returned.

### validate_data()

```python
validation = tsmeta.validate_data(df)

print(validation.summary())
validation_details = validation.to_dict()
```

`validate_data()` accepts a pandas DataFrame and returns a `ValidationReport`.
It does not modify the input DataFrame.

### clean_data()

```python
cleaning = tsmeta.clean_data(
    df,
    insert_missing_timestamps=True,
    interpolation_method="linear",
)

cleaned_df = cleaning.data
print(cleaning.summary())
cleaning_details = cleaning.to_dict()
```

`clean_data()` accepts a pandas DataFrame and returns a `CleaningResult`
containing a cleaned DataFrame and a cleaning report. It does not modify the
original input DataFrame.

Cleaned data can be saved to CSV or Excel:

```python
cleaning.save("cleaned_sales.csv")
cleaning.save("cleaned_sales.xlsx")
```

### analyze()

```python
analysis = tsmeta.analyze(df)

print(analysis.summary())
analysis_details = analysis.to_dict()
```

`analyze()` accepts a pandas DataFrame and returns an `AnalysisResult`
containing a `DatasetAnalysis` report. It computes dataset-level statistics
without modifying the input DataFrame.

## Public API

The package exposes the following public API from `tsmeta`:

- `load_data`
- `validate_data`
- `ValidationReport`
- `clean_data`
- `CleaningResult`
- `CleaningReport`
- `analyze`
- `AnalysisResult`
- `DatasetAnalysis`

## Current Capabilities

TSMeta can load CSV files, Excel files, and pandas DataFrames. It can validate
generic dataset properties, perform basic time-series validation for native
pandas datetime columns, clean common structural and data quality issues, and
compute dataset-level analysis statistics. Cleaning returns an independent
cleaned DataFrame and metadata. Validation and analysis inspect the input data
without modifying it.

## Current Scope

- Works with pandas DataFrames.
- Supports CSV and Excel input.
- Performs dataset validation.
- Performs basic time-series validation.
- Cleans datasets without modifying the original input.
- Computes dataset-level statistics.
- Does not modify input data during validation or analysis.
- Assumes at most one datetime column for Version 1 behavior.
- Does not support multiple independent time series.

## Project Structure

```text
TSMeta/
  tsmeta/
    __init__.py
    analysis.py
    cleaning.py
    loader.py
    validation.py
  tests/
    test_analysis.py
    test_cleaning.py
    test_loader.py
    test_package.py
    test_validation.py
  README.md
  PROJECT.md
  ROADMAP.md
  pyproject.toml
```

## Development

Run the quality checks:

```bash
ruff check .
black --check .
pytest
```

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and
follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

TSMeta is licensed under the [MIT License](LICENSE).
