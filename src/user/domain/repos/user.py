from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr

from src.user.domain.models.user import User


class UserRepo(ABC):
    @abstractmethod
    def insert(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: EmailStr) -> Optional[User]:
        pass
