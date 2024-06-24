from datetime import date
from uuid import UUID

from pydantic import BaseModel


class CreateScheduleSchema(BaseModel):
    start_date: date
    end_date: date
    availability_id: UUID
