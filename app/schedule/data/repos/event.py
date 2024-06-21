from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.schedule.data.models.event import EventModel
from app.schedule.domain.models.event import Event
from app.schedule.domain.repos.event import EventRepo


class EventRepoImpl(EventRepo):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, obj: Event) -> Event:
        record = EventModel(**obj.dict())
        record.id = str(record.id)
        record.availability_id = str(record.availability_id)
        self.session.add(record)
        return Event(**record.dict())

    def get(self, id: UUID) -> Optional[Event]:
        return (
            self.session.query(EventModel)
            .filter(
                EventModel.id == str(id),
            )
            .first()
        )
