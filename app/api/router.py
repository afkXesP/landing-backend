from fastapi import APIRouter

from .contact import router as contact_router
from .health import router as health_router
from .metrics import router as metrics_router


api_router = APIRouter(prefix="/api")

api_router.include_router(contact_router)
api_router.include_router(health_router)
api_router.include_router(metrics_router)