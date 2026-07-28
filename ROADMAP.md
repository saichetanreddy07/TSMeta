# TSMeta Roadmap

This document outlines the planned evolution of TSMeta.

The roadmap is subject to change as the project grows.

---

# Vision

Build an open-source Python library for intelligent time-series analysis, forecasting model recommendation, forecasting, benchmarking, visualization, and reporting.

The goal is to simplify the end-to-end forecasting workflow while following professional software engineering practices.

---

# Version Roadmap

## v0.1.0 — Project Foundation

Status: In Progress

### Goals

- Repository setup
- Python package structure
- Documentation
- Public API design
- Development tooling
- GitHub Actions
- Testing framework

---

## v0.2.0 — Data Loading & Validation

### Features

- CSV Loader
- Excel Loader
- Pandas DataFrame support
- Datetime detection
- Frequency detection
- Dataset validation
- Missing value checks
- Duplicate timestamp detection

---

## v0.3.0 — Dataset Analysis

### Features

- Dataset summary
- Statistical overview
- Trend detection
- Seasonality hints
- Stationarity tests
- Missing value report
- Dataset profiling

---

## v0.4.0 — Meta-feature Extraction

### Features

Extract statistical meta-features including

- Mean
- Variance
- Standard deviation
- Skewness
- Kurtosis
- Trend strength
- Seasonality strength
- Entropy
- Autocorrelation
- Dataset length
- Missing ratio

---

## v0.5.0 — Recommendation Engine

### Features

Recommend suitable forecasting models based on extracted meta-features.

Initial supported models

- ARIMA
- ETS
- Prophet
- Linear Regression
- Random Forest

Future versions may support additional forecasting models.

---

## v0.6.0 — Forecasting

### Features

Unified forecasting interface.

Users should be able to write

```python
forecast = tsmeta.forecast(df)
```

Support

- Automatic model selection
- Manual model selection
- Configurable forecast horizon

---

## v0.7.0 — Benchmarking

### Features

Compare forecasting models using

- MAE
- RMSE
- MAPE
- R² (where applicable)

Generate comparison tables.

---

## v0.8.0 — Visualization

### Features

Generate plots including

- Forecast plots
- Trend plots
- Seasonality plots
- Residual analysis
- Model comparison charts

---

## v0.9.0 — Reporting

### Features

Generate comprehensive reports.

Possible outputs

- HTML
- Markdown
- PDF

---

## v1.0.0 — Stable Release

### Goals

- Stable public API
- Complete documentation
- Comprehensive testing
- Continuous Integration
- Example notebooks
- Production-ready release

---

# Future Ideas

Potential future additions include

- Deep Learning forecasting
- Hierarchical forecasting
- Probabilistic forecasting
- Explainable recommendations
- AutoML integration
- Time-series anomaly detection
- Interactive dashboards
- CLI support
- Plugin architecture

---

# Development Philosophy

Every release should

- Improve usability
- Maintain backwards compatibility whenever possible
- Keep the public API simple
- Prioritize maintainability over complexity
