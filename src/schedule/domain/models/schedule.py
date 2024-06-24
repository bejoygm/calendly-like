from typing import List
import uuid

from pydantic import BaseModel, EmailStr, Field


class Schedule(BaseModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    rules: List
    timezone: str
    user_id: uuid.UUID
