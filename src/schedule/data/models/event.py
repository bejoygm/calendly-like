from src.utils import generate_uuid
from src.database import Base
from datetime import datetime, timezone, date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class EventModel(Base):
    __tablename__ = "event"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(nullable=False)
    availability_id: Mapped[str] = mapped_column(ForeignKey("availability.id"))
    duration: Mapped[int] = mapped_column(nullable=False)
    starts_from: Mapped[date] = mapped_column(nullable=False)
    ends_at: Mapped[date] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "availability_id": self.availability_id,
            "starts_from": self.starts_from,
            "ends_at": self.ends_at,
        }
