"""Public interface for TSMeta."""

from importlib.metadata import PackageNotFoundError, version

from tsmeta.analysis import AnalysisResult, DatasetAnalysis, analyze
from tsmeta.cleaning import CleaningReport, CleaningResult, clean_data
from tsmeta.loader import load_data
from tsmeta.validation import ValidationReport, validate_data

try:
    __version__ = version("tsmeta")
except PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = [
    "AnalysisResult",
    "CleaningReport",
    "CleaningResult",
    "DatasetAnalysis",
    "ValidationReport",
    "__version__",
    "analyze",
    "clean_data",
    "load_data",
    "validate_data",
]
