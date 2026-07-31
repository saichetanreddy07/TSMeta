"""Public interface for TSMeta."""

from tsmeta.analysis import AnalysisResult, DatasetAnalysis, analyze
from tsmeta.cleaning import CleaningReport, CleaningResult, clean_data
from tsmeta.loader import load_data
from tsmeta.validation import ValidationReport, validate_data

__all__ = [
    "AnalysisResult",
    "CleaningReport",
    "CleaningResult",
    "DatasetAnalysis",
    "ValidationReport",
    "analyze",
    "clean_data",
    "load_data",
    "validate_data",
]
