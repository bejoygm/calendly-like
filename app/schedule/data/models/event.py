from app.base.data.models.base import Base, generate_uuid
from datetime import datetime

from sqlalchemy import JSON, Column, String, ForeignKey, DateTime, func, Date
from sqlalchemy.orm import Mapped, mapped_column


class EventModel(Base):
    __tablename__ = "event"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    availability_id = mapped_column(ForeignKey("availability.id"))
    duration: Mapped[int] = mapped_column(nullable=False)
    starts_from = Column(Date, nullable=False)
    ends_at = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "availability_id": self.availability_id,
            "starts_from": self.starts_from,
            "ends_at": self.ends_at,
        }
