from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.schedule.data.models.availability import AvailabilityModel
from app.schedule.domain.models.availability import Availability
from app.schedule.domain.repos.availability import AvailabilityRepo
from app.user.domain.models.user import User


class AvailabilityRepoImpl(AvailabilityRepo):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, obj: Availability) -> Availability:
        record = AvailabilityModel(**obj.dict())
        record.id = str(record.id)
        record.rules
        record.user_id = str(record.user_id)
        self.session.add(record)
        return Availability(**record.dict())

    def get(self, id: UUID) -> Optional[Availability]:
        return (
            self.session.query(AvailabilityModel)
            .filter(
                AvailabilityModel.id == str(id),
            )
            .first()
        )
