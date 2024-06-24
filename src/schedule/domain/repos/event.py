from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.schedule.domain.models.event import Event


class EventRepo(ABC):
    @abstractmethod
    def insert(self, obj: Event) -> Optional[Event]:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[Event]:
        pass
