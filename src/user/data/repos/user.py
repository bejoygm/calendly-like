from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from sqlalchemy.orm import Session
from src.user.domain.models.user import User
from src.user.domain.repos.user import UserRepo
from src.user.data.models.user import User as UserModel


class UserRepoImpl(UserRepo):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, user: User) -> User:
        record = UserModel(**user.model_dump())
        record.id = str(record.id)
        self.session.add(record)
        return User(**record.dict())

    def get_by_email(self, email: EmailStr) -> Optional[User]:
        user = (
            self.session.query(UserModel)
            .filter(
                UserModel.email == email,
            )
            .first()
        )

        if user:
            return User(**user.dict())
        return None

    def get(self, id: UUID) -> Optional[User]:
        user = (
            self.session.query(UserModel)
            .filter(
                UserModel.id == str(id),
            )
            .first()
        )

        if user:
            return User(**user.dict())
        return None
