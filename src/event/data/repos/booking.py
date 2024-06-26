from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.event.data.models.booking import BookingModel
from src.event.domain.models.booking import Booking
from src.event.domain.repos.booking import BookingRepo


class BookingRepoImpl(BookingRepo):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, obj: Booking) -> Booking:
        record = BookingModel(**obj.model_dump())
        record.id = str(record.id)
        record.event_id = str(record.event_id)
        record.booked_by_id = str(record.booked_by_id)
        record.booked_for_id = str(record.booked_for_id)
        self.session.add(record)
        return Booking(**record.dict())

    def filter_by_user_id(self, user_id: UUID) -> List[Booking]:
        bookings = self.session.query(BookingModel).filter(
            or_(
                BookingModel.booked_by_id == str(user_id),
                BookingModel.booked_for_id == str(user_id),
            )
        )
        return [Booking(**b.dict()) for b in bookings]
