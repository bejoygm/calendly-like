import uuid

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    name: str
    email: EmailStr
