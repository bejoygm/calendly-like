from sqlalchemy.orm import Session

from src.schedule.domain.repos.availability import AvailabilityRepo
from src.user.domain.models.user import User


class CreateScheduleUsecase:
    def __init__(self, availability_repo: AvailabilityRepo):
        self.availability_repo = availability_repo
