from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.event.data.models.event import EventModel
from src.event.domain.models.event import Event
from src.event.domain.repos.event import EventRepo


class EventRepoImpl(EventRepo):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, obj: Event) -> Event:
        record = EventModel(**obj.model_dump())
        record.id = str(record.id)
        record.availability_id = str(record.availability_id)
        self.session.add(record)
        return Event(**record.dict())

    def get(self, id: UUID) -> Optional[Event]:
        event = (
            self.session.query(EventModel)
            .filter(
                EventModel.id == str(id),
            )
            .first()
        )
        if event:
            return Event(**event.dict())

        return None
