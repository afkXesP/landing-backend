from fastapi import APIRouter, status

from .dependencies import ContactServiceDependency
from app.schemas import MetricsResponse


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)

@router.get("", response_model=MetricsResponse, status_code=status.HTTP_200_OK)
def get_metrics(service: ContactServiceDependency) -> MetricsResponse:
    return service.get_metrics()

