import uuid
from typing import List

from pydantic import BaseModel, Field


class Availability(BaseModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    name: str
    rules: List
    timezone: str
    user_id: uuid.UUID
