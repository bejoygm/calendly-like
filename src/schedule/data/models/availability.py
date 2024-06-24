from datetime import datetime, timezone
from typing import Any
from src.utils import generate_uuid
from src.database import Base
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class AvailabilityModel(Base):
    __tablename__ = "availability"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    rules: Mapped[dict[str, Any]] = mapped_column(nullable=False)
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
            "user_id": self.user_id,
            "rules": self.rules,
            "timezone": self.timezone,
        }
