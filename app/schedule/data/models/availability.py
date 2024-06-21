from app.base.data.models.base import Base, generate_uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column


class AvailabilityModel(Base):
    __tablename__ = "availability"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = mapped_column(ForeignKey("user.id"))
    rules = Column(JSON, nullable=False)
    timezone = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
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
