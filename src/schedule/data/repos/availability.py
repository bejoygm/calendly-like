from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.schedule.data.models.availability import AvailabilityModel
from src.schedule.domain.models.availability import Availability
from src.schedule.domain.repos.availability import AvailabilityRepo


class AvailabilityRepoImpl(AvailabilityRepo):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, obj: Availability) -> Availability:
        record = AvailabilityModel(**obj.model_dump())
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
