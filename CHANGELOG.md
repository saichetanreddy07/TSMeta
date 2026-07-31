# Changelog

All notable changes to TSMeta are documented in this file.

## v0.1.0 - Beta

Initial beta release of TSMeta.

### Added

- Public package API for loading, validating, cleaning, and analyzing datasets.
- CSV, Excel, and pandas DataFrame input support through `load_data()`.
- Generic dataset validation through `validate_data()` and `ValidationReport`.
- Basic time-series validation for native pandas datetime columns.
- Dataset cleaning through `clean_data()`, `CleaningResult`, and
  `CleaningReport`.
- Structural cleaning, data type cleaning, missing value handling, timestamp
  sorting, optional timestamp insertion, and interpolation options.
- Phase 1 dataset analysis through `analyze()`, `AnalysisResult`, and
  `DatasetAnalysis`.
- Dataset-level analysis statistics including row and column counts, dtype
  counts, missing value percentage, duplicate row percentage, and memory usage.
- Example scripts for the basic workflow, DataFrame input, and cleaning options.
