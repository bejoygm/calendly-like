import zoneinfo
from datetime import time
from enum import Enum
from typing import List
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_serializer,
    field_validator,
)
from pydantic_core.core_schema import FieldValidationInfo

all_zones = zoneinfo.available_timezones()
tz_dict: dict = {}
for tz_name in all_zones:
    tz_dict[tz_name.replace("/", "_").replace("-", "_")] = tz_name


Timezone = Enum("Timezone", tz_dict)


class Day(str, Enum):
    sun = "sun"
    mon = "mon"
    tue = "tue"
    wed = "wed"
    thu = "thu"
    fri = "fri"
    sat = "sat"


class Interval(BaseModel):
    from_: time = Field(alias="from", examples=["15:00"])
    to: time = Field(examples=["15:30"])

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_validator("to")
    def validate_duration(cls, to, info: FieldValidationInfo):
        from_ = info.data["from_"]

        if to < from_:
            raise ValueError("`to` must be greater than `from`")

        return to

    @field_serializer("from_")
    def serialize_from_(self, t: time, _info):
        return t.strftime("%H:%M")

    @field_serializer("to")
    def serialize_to(self, t: time, _info):
        return t.strftime("%H:%M")


class Duration(BaseModel):
    day: Day
    intervals: List[Interval]

    model_config = ConfigDict(
        use_enum_values=True,
    )


class SetAvailabilitySchema(BaseModel):
    rules: List[Duration]
    timezone: Timezone
    email: EmailStr

    model_config = ConfigDict(
        use_enum_values=True,
    )

    # todo: handle conflicting intervals
    @field_validator("rules")
    def validate_intervals(cls, v):
        return v


class SetAvailabilityResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    rules: List[Duration]
    timezone: Timezone
