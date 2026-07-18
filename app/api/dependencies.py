from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from functools import lru_cache

from app.db import get_db
from app.repositories import ContactRepository
from app.services.ai_service import AIService
from app.services.contact_service import ContactService
from app.services.email_service import EmailService


def  get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(
        db=db, repository=ContactRepository(db=db), ai_service=AIService(), email_service=EmailService()
    )


def get_contact_repository(db: Session = Depends(get_db)) -> ContactRepository:
    return ContactRepository(db=db)


@lru_cache
def get_ai_service() -> AIService:
    return AIService()


@lru_cache
def get_email_service() -> EmailService:
    return EmailService()


ContactServiceDependency = Annotated[
    ContactService,
    Depends(get_contact_service),
]