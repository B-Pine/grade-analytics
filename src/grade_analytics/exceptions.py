class GradeAnalyticsError(Exception):
    """Base exception for the whole project."""


class InvalidScoreError(GradeAnalyticsError):
    """Raised when score is not between 0 - 100."""