import smtplib

from email.message import EmailMessage

from app.core.config import settings
from app.core.logging import get_logger


logger = get_logger(__name__)


class EmailService:
    @staticmethod
    def _create_message(*, recipient: str, subject: str, body: str) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = settings.SMTP_FROM
        message["To"] = recipient
        message.set_content(body)

        return message

    def _send_email(self, *, message: EmailMessage) -> bool:
        if not settings.SMTP_HOST:
            logger.warning("SMTP server is not configured.")
            return False

        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                smtp.send_message(message)

            logger.info("Email '%s' sent to %s",message["Subject"],message["To"])
            return True

        except Exception:
            logger.exception("Failed to send email to %s",message["To"])
            return False

    def send_owner_notification(self, *, name: str) -> bool:
        subject = "New contact request"
        body = (
            f"Hello, {name}!\n\n"
            "Thank you for contacting us.\n\n"
            "We have received your request and "
            "will get back to you as soon as possible."
        )

        message = self._create_message(
            recipient=settings.OWNER_EMAIL,
            subject=subject,
            body=body,
        )

        return self._send_email(message=message)

    def send_confirmation(self, *, recipient: str, name: str) -> bool:
        subject = "Your request has been received"

        body = (f"Hello, {name}!\n\n" 
                "Thank you for contacting us.\n"
                "We have received your request and will get back to you as soon as possible.")

        message = self._create_message(
            recipient=recipient,
            subject=subject,
            body=body,
        )

        return self._send_email(message=message)
