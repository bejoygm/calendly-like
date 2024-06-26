from src.event.domain.models.availability import Availability
from src.event.domain.repos.availability import AvailabilityRepo


class CreateAvailabilityUsecase:
    def __init__(
        self,
        availability_repo: AvailabilityRepo,
    ):
        self.repo = availability_repo

    def execute(self, availability: Availability) -> Availability:
        return self.repo.insert(availability)
