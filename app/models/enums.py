from enum import StrEnum


class RequestCategory(StrEnum):
    UNKNOWN = "unknown"
    SALES = "sales"
    SUPPORT = "support"
    OTHER = "other"


class Sentiment(StrEnum):
    UNKNOWN = "unknown"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
