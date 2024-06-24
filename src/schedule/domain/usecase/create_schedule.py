from src.schedule.domain.repos.availability import AvailabilityRepo


class CreateScheduleUsecase:
    def __init__(self, availability_repo: AvailabilityRepo):
        self.availability_repo = availability_repo
