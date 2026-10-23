"""Custom exceptions raised by the grade_analytics package."""


class GradeAnalyticsError(Exception):
    """Base class for all errors raised by grade_analytics.

    Catch this to handle any error from the package in one place.
    """


class InvalidScoreError(GradeAnalyticsError):
    """Raised when a score falls outside the valid 0 - 100 range."""


class DataFileError(GradeAnalyticsError):
    """Raised when a data file cannot be found, read or written."""


class InvalidRecordError(GradeAnalyticsError):
    """Raised when a CSV row has missing or invalid values."""


class InsufficientDataError(GradeAnalyticsError):
    """Raised when a calculation needs at least one value but got none."""
