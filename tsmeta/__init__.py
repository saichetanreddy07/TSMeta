"""Public interface for TSMeta."""

from tsmeta.loader import load_data
from tsmeta.validation import ValidationReport, validate_data

__all__ = ["load_data", "validate_data", "ValidationReport"]
