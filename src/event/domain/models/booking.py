import uuid

from pydantic import AwareDatetime, BaseModel, Field


class Booking(BaseModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    spot: AwareDatetime
    event_id: uuid.UUID
    booked_by_id: uuid.UUID
    booked_for_id: uuid.UUID
    timezone: str
