# AGENTS.md

This document provides instructions for AI coding assistants contributing to TSMeta.

---

# Project Overview

TSMeta is an open-source Python library for intelligent time-series analysis, forecasting model recommendation, forecasting, benchmarking, visualization, and reporting.

The project follows modern Python software engineering practices.

Always prioritize readability, maintainability, and modularity.

---

# General Principles

Always

- Write production-quality code.
- Keep functions small and focused.
- Use descriptive names.
- Add type hints.
- Add Google-style docstrings.
- Follow PEP 8.
- Write modular code.
- Prefer composition over duplication.

Never

- Write unnecessary comments.
- Introduce breaking API changes.
- Modify unrelated files.
- Add unnecessary dependencies.
- Generate placeholder implementations unless requested.
- Use print() inside library code.

---

# Public API

The public API should remain simple.

Preferred usage

```python
import tsmeta

df = tsmeta.load_data("sales.csv")

analysis = tsmeta.analyze(df)

recommendation = tsmeta.recommend(df)

forecast = tsmeta.forecast(df)

benchmark = tsmeta.benchmark(df)
```

Avoid exposing internal helper functions.

---

# Repository Structure

```
tsmeta/
    analysis/
    preprocessing/
    feature_extraction/
    recommendation/
    forecasting/
    benchmarking/
    visualization/
    reports/
    utils/
```

Every module should have one responsibility.

---

# Coding Standards

Python Version

- Python 3.11+

Formatting

- Ruff compatible
- Black compatible

Documentation

- Google-style docstrings

Typing

- Type hints for all public functions

Maximum preferred function length

Approximately 50 lines.

Split larger functions into reusable helpers.

---

# Error Handling

Raise meaningful exceptions.

Prefer

- FileNotFoundError
- ValueError
- TypeError

Provide informative error messages.

Never silently ignore errors.

---

# Logging

Use the standard logging module.

Never use print() inside library code.

---

# Dependencies

Prefer the standard library whenever possible.

Avoid introducing new third-party dependencies without clear justification.

Current planned dependencies

- pandas
- numpy
- scipy
- scikit-learn
- statsmodels
- matplotlib

---

# Testing

Every public feature should include tests.

Tests should cover

- Valid inputs
- Invalid inputs
- Edge cases

Testing framework

- pytest

---

# Documentation

Every public function should include

- Summary
- Parameters
- Returns
- Raises

Examples should be added where appropriate.

---

# Performance

Prefer vectorized operations over loops.

Avoid repeated computations.

Design for scalability.

---

# Architecture

The processing pipeline is

Dataset

↓

Validation

↓

Analysis

↓

Meta-feature Extraction

↓

Recommendation

↓

Forecasting

↓

Benchmarking

↓

Visualization

↓

Reporting

Keep each stage independent.

---

# AI Contribution Rules

Before implementing new functionality

1. Read PROJECT.md.
2. Follow ROADMAP.md.
3. Preserve the existing public API.
4. Keep implementations modular.
5. Avoid unnecessary complexity.

When modifying existing code

- Preserve backwards compatibility whenever possible.
- Minimize unrelated changes.
- Keep commits focused on a single feature.

---

# Code Generation Guidelines

Generated code should

- Be production-ready.
- Be readable.
- Include tests when applicable.
- Include docstrings.
- Include type hints.
- Follow the existing project structure.
- Avoid overengineering.

Always optimize for long-term maintainability rather than short-term convenience.
