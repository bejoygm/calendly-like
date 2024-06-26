import uuid
from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class SpotAvailability(str, Enum):
    available = "available"
    unavailable = "unavailable"


class Event(BaseModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    name: str
    availability_id: uuid.UUID
    starts_from: date
    ends_at: date
    duration: int
    description: str
