# Contributing to TSMeta

Thank you for considering a contribution to TSMeta. This project welcomes bug
reports, documentation improvements, tests, and feature proposals.

## Before You Start

Please review [PROJECT.md](PROJECT.md) and [ROADMAP.md](ROADMAP.md). Keep
contributions aligned with the current milestone and preserve the planned public
API. New functionality should not be added ahead of its roadmap milestone unless
it has been discussed first.

## Development Setup

TSMeta supports Python 3.11 and later.

```bash
git clone <repository-url>
cd TSMeta
python -m venv .venv
python -m pip install -e ".[dev]"
```

Before opening a pull request, run:

```bash
ruff check .
black --check .
pytest
```

## Pull Requests

- Keep each pull request focused on one concern.
- Include tests for every public feature, covering valid, invalid, and edge cases.
- Add type hints and Google-style docstrings to public functions.
- Use clear, descriptive commit messages and pull request descriptions.
- Do not introduce dependencies without a clear project need.
- Do not change the public API without prior discussion.

## Reporting Issues

Please include the Python version, operating system, a minimal reproducible
example, expected behavior, and actual behavior. Do not include sensitive data.

## Code of Conduct

All participants must follow the [Code of Conduct](CODE_OF_CONDUCT.md).
