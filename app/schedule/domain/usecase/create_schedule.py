from sqlalchemy.orm import Session

from app.schedule.domain.repos.availability import AvailabilityRepo
from app.user.domain.models.user import User
from app.user.domain.repos.user import UserRepo


class CreateScheduleUsecase:
    def __init__(
        self, availability_repo: AvailabilityRepo, schedule_repo: ScheduleRepo
    ):
        self.availability_repo = availability_repo
        self.schedule_repo = schedule_repo

    def execute(self, user: User):
        return self.repo.insert(user)
