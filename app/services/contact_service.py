from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models import ContactRequest
from app.repositories import ContactRepository
from app.schemas import ContactRequestCreate, ContactResponse, MetricsResponse
from .ai_service import AIService
from .email_service import EmailService


logger = get_logger(__name__)


class ContactService:
    def __init__(self, db: Session, repository: ContactRepository, ai_service: AIService, email_service: EmailService):
        self.db = db
        self.repository = repository
        self.ai_service = ai_service
        self.email_service = email_service

    def create(self, data: ContactRequestCreate) -> ContactResponse:
        category = self.ai_service.classify(data.message)
        contact = ContactRequest(
            name=data.name,
            email=data.email,
            phone=data.phone,
            message=data.message,
            category=category
        )

        try:
            self.repository.create(contact)
            self.db.commit()

            owner_sent = self.email_service.send_owner_notification(name=contact.name)
            confirmation_sent = self.email_service.send_confirmation(recipient=contact.email, name=contact.name)

            logger.info(
                "Contact request #%s created (owner_email=%s, confirmation=%s)",
                contact.id,
                owner_sent,
                confirmation_sent,
            )

            return ContactResponse(status="success", message="Request successfully received.", request_id=contact.id)

        except Exception:
            self.db.rollback()
            logger.exception("Failed to create contact request")

            raise

    def get_metrics(self) -> MetricsResponse:
        return MetricsResponse(
            total_requests=self.repository.count(), categories=self.repository.get_category_counts()
        )
