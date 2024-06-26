from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.utils import generate_uuid


class BookingModel(Base):
    __tablename__ = "booking"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    spot: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    booked_by_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    booked_for_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"))
    timezone: Mapped[str] = mapped_column(nullable=False)
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
            "spot": self.spot.astimezone(ZoneInfo(self.timezone)),
            "event_id": self.event_id,
            "booked_by_id": self.booked_by_id,
            "booked_for_id": self.booked_for_id,
            "timezone": self.timezone,
        }
