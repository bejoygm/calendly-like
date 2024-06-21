from abc import ABC, abstractmethod
from typing import Optional, Sequence
from uuid import UUID

from app.schedule.domain.models.event import Event


class EventRepo(ABC):
    @abstractmethod
    def insert(self, obj: Event) -> Optional[Event]:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[Event]:
        pass
