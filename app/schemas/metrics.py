from pydantic import BaseModel


class MetricsResponse(BaseModel):
    total_requests: int
    categories: dict[str, int]
