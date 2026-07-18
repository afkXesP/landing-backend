from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


from app.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.limiter import limiter
from app.core.exceptions import global_exception_handler
from app.db import Base, engine


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path("storage").mkdir(parents=True, exist_ok=True)

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.state.limiter = limiter

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)

app.include_router(api_router)