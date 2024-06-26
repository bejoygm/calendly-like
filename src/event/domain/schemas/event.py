from datetime import date, datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, AwareDatetime
from pydantic_core.core_schema import ValidationInfo

from src.event.domain.models.event import SpotAvailability


class CreateEventSchema(BaseModel):
    name: str
    starts_from: date
    ends_at: date
    duration: int = Field(..., ge=15)  # can make this configurable later on
    availability_id: UUID
    description: str

    @field_validator("ends_at")
    def validate_ends_at(cls, ends_at, info: ValidationInfo):
        starts_from = info.data["starts_from"]

        if ends_at < starts_from:
            raise ValueError("ends_at must be greater than or equal to starts_from")
        return ends_at


class CreateEventResponseSchema(CreateEventSchema):
    id: UUID


class Spots(BaseModel):
    status: SpotAvailability
    start_time: AwareDatetime


class DayAvailability(BaseModel):
    date: date
    spots: List[Spots]


class GetEventCalendar(BaseModel):
    timezone: str
    days: List[DayAvailability]


class BookEventSpotRequestSchema(BaseModel):
    spot: AwareDatetime
    user_id: UUID
    timezone: str


class BookEventSpotResponseSchema(BaseModel):
    id: UUID
    spot: AwareDatetime
    event_id: UUID
    booked_by_id: UUID
    booked_for_id: UUID
    timezone: str
