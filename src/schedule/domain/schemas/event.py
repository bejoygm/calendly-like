from typing import List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from datetime import date, datetime

from src.schedule.domain.models.event import SpotAvailability


class CreateEventSchema(BaseModel):
    name: str
    starts_from: date
    ends_at: date
    duration: int = Field(..., ge=5)
    availability_id: UUID

    @field_validator("ends_at")
    def validate_ends_at(cls, ends_at, info: FieldValidationInfo):
        starts_from = info.data["starts_from"]

        if ends_at < starts_from:
            raise ValueError("ends_at must be greater than or equal to starts_from")
        return ends_at


class CreateEventResponseSchema(CreateEventSchema):
    id: UUID


class Spots(BaseModel):
    status: SpotAvailability
    start_time: datetime


class DayAvailability(BaseModel):
    date: datetime
    spots: List[Spots]


class GetEventCalendar(BaseModel):
    timezone: str
    days: List[DayAvailability]
