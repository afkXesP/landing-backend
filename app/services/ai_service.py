from google import genai

from app.core.config import settings
from app.core.logging import get_logger
from app.models.enums import RequestCategory
from app.prompts import CLASSIFICATION_PROMPT


logger = get_logger(__name__)


class AIService:
    _client = None

    @property
    def client(self):
        if self._client is None:
            self._client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        return self._client

    def classify(self, message: str) -> RequestCategory:
        """
        Определяет категорию обращения
        """
        if not settings.GOOGLE_API_KEY:
            logger.warning("GOOGLE_API_KEY is missing")
            return RequestCategory.UNKNOWN

        prompt = CLASSIFICATION_PROMPT.format(message=message)

        try:
            response = self.client.interactions.create(model=settings.GEMINI_MODEL, input=prompt)
            logger.info("Gemini raw response: %r", response.output_text)

            category = response.output_text.strip().lower().replace(".", "")
            mapping = {
                "sales": RequestCategory.SALES,
                "support": RequestCategory.SUPPORT,
                "other": RequestCategory.OTHER,
            }

            return mapping.get(category, RequestCategory.UNKNOWN)


        except Exception:
            logger.exception(f"Failed to classify request")
            return RequestCategory.UNKNOWN
