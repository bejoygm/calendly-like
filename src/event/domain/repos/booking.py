from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.event.domain.models.booking import Booking


class BookingRepo(ABC):
    @abstractmethod
    def insert(self, obj: Booking) -> Booking:
        pass

    @abstractmethod
    def filter_by_user_id(self, user_id: UUID) -> List[Booking]:
        pass
