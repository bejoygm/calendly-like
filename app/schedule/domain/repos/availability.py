from abc import ABC, abstractmethod
from typing import Optional, Sequence
from uuid import UUID

from app.schedule.domain.models.availability import Availability
from app.user.domain.models.user import User


class AvailabilityRepo(ABC):
    @abstractmethod
    def insert(self, obj: Availability) -> Optional[Availability]:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[Availability]:
        pass
