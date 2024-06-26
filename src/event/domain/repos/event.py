from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.event.domain.models.event import Event


class EventRepo(ABC):
    @abstractmethod
    def insert(self, obj: Event) -> Event:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[Event]:
        pass
