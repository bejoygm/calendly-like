from app.base.data.models.base import Base, generate_uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
        }
