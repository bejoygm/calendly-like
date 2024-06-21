from typing import Optional, Sequence
import uuid

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.user.domain.models.user import User
from app.user.domain.repos.user import UserRepo
from app.user.data.models.user import UserModel


class UserRepoImpl(UserRepo):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, user: User) -> User:
        record = UserModel(**user.dict())
        record.id = str(record.id)
        self.session.add(record)
        return User(**record.dict())

    def get_by_email(self, email: EmailStr) -> Optional[User]:
        return (
            self.session.query(UserModel)
            .filter(
                UserModel.email == email,
            )
            .first()
        )
