# TSMeta

TSMeta is an open-source Python library for intelligent time-series analysis,
forecasting model recommendation, forecasting, benchmarking, visualization, and
reporting.

The project aims to provide a simple, unified interface for common forecasting
workflows while building on established scientific Python libraries rather than
replacing them.

## Status

TSMeta is in its early development phase. CSV and Excel data loading are
available; dataset validation, analysis, forecasting, and the remaining planned
features are not yet implemented. See the [roadmap](ROADMAP.md) for the planned
sequence of work.

## Planned API

```python
import tsmeta

df = tsmeta.load_data("sales.csv")
```

The remaining planned public API will add analysis, recommendation, forecasting,
and benchmarking in later roadmap milestones.

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
