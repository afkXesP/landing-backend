from fastapi import APIRouter, status, Request

from .dependencies import ContactServiceDependency
from app.schemas import ContactRequestCreate, ContactResponse
from app.core.limiter import limiter
from app.core.config import settings


router = APIRouter(
    prefix="/contact",
    tags=["Contact"],
)


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT)
def create_contact(request: Request, data: ContactRequestCreate, service: ContactServiceDependency) -> ContactResponse:
    return service.create(data)
