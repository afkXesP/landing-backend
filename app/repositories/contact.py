from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ContactRequest


class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, contact: ContactRequest) -> ContactRequest:
        self.db.add(contact)
        self.db.flush()
        self.db.refresh(contact)

        return contact

    def count(self) -> int:
        stmt = select(func.count(ContactRequest.id))
        return self.db.scalar(stmt) or 0

    def get_category_counts(self) -> dict[str, int]:
        stmt = (
            select(ContactRequest.category, func.count(ContactRequest.id))
            .group_by(ContactRequest.category)
        )

        result = self.db.execute(stmt).all()

        return dict(
            sorted(
                ((category.value, count) for category, count in result),
                key=lambda x: x[0],
            )
        )
