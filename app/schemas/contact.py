from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .enums import ResponseStatus


Phone = Annotated[str, Field(pattern=r"^\+?[0-9()\-\s]{7,30}$")]


class ContactRequestCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: Phone
    message: str = Field(min_length=10, max_length=5000)


class ContactResponse(BaseModel):
    status: ResponseStatus
    message: str
    request_id: int