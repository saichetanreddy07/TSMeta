# TSMeta

TSMeta is an open-source Python library for preparing time-series datasets and,
in future releases, analyzing them, recommending forecasting models, producing
forecasts, benchmarking models, visualizing results, and generating reports.

The project aims to provide a simple, unified interface for common forecasting
workflows while building on established scientific Python libraries rather than
replacing them.

## Status

TSMeta currently provides data loading, generic and time-series validation, and
data cleaning. Analysis, recommendation, forecasting, benchmarking,
visualization, and reporting remain planned. See the [roadmap](ROADMAP.md) for
the planned sequence of work.

## Current Workflow

```text
load_data()
    ↓
validate_data()
    ↓
clean_data()
    ↓
analyze() (planned)
    ↓
recommend() (planned)
    ↓
forecast() (planned)
```

Each implemented stage is independent: loading returns a DataFrame, validation
inspects it without modification, and cleaning returns a new DataFrame.

## Features

### Loader

- Load CSV files.
- Load Excel workbooks (`.xlsx` and `.xls`).
- Accept an existing pandas DataFrame and return a copy.

### Validation

- Generic shape, duplicate-row, missing-value, and dtype inspection.
- Time-series inspection for native pandas datetime columns, timestamp
  duplicates, ordering, inferred frequency, and univariate or multivariate
  structure.
- `ValidationReport` with `summary()` and `to_dict()` methods.

### Cleaning

- Structural cleaning: duplicate and empty row/column removal, standardized
  column names, and index reset.
- Data-type cleaning: datetime and numeric conversion plus string trimming.
- Missing-value handling: numeric mean and categorical mode filling while
  preserving datetime `NaT` values.
- Time-series cleaning for one datetime column: sorting, missing-timestamp
  detection, optional insertion, and linear/forward/backward filling.
- `CleaningReport` and `CleaningResult`, each with `summary()` and `to_dict()`.
- `CleaningResult.save()` support for CSV and Excel output.

## Usage

### Load data

```python
import tsmeta

df = tsmeta.load_data("sales.csv")
```

`load_data()` also accepts `.xlsx`, `.xls`, `pathlib.Path`, and an existing
`pandas.DataFrame`.

### Validate data

```python
report = tsmeta.validate_data(df)

print(report.summary())
validation_details = report.to_dict()
```

`ValidationReport` describes generic dataset properties and, when exactly one
native pandas datetime column is present, time-series properties.

### Clean data

```python
result = tsmeta.clean_data(
    df,
    insert_missing_timestamps=True,
    interpolation_method="linear",
)

cleaned_df = result.data
print(result.summary())
cleaning_details = result.to_dict()
```

### Export cleaned data

```python
result.save("cleaned_sales.csv")
result.save("cleaned_sales.xlsx")
```

## Project Structure

```text
TSMeta/
├── tsmeta/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── loader.py
│   └── validation.py
├── tests/
│   ├── test_cleaning.py
│   ├── test_loader.py
│   ├── test_package.py
│   └── test_validation.py
├── README.md
├── PROJECT.md
├── ROADMAP.md
└── pyproject.toml
```

## Development

TSMeta requires Python 3.11 or later. Create an environment and install the
development tools:

```bash
python -m pip install -e ".[dev]"
```

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
