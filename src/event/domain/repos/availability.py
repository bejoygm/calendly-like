from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.event.domain.models.availability import Availability


class AvailabilityRepo(ABC):
    @abstractmethod
    def insert(self, obj: Availability) -> Availability:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[Availability]:
        pass
