from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from .enums import RequestCategory, Sentiment


class ContactRequest(Base):
    __tablename__ = 'contact_request'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(30))
    message: Mapped[str] = mapped_column(Text)

    category: Mapped[str] = mapped_column(String(50), default=RequestCategory.UNKNOWN)
    sentiment: Mapped[str] = mapped_column(String(30), default=Sentiment.UNKNOWN)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
