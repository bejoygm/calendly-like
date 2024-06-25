from datetime import date
from uuid import UUID

from src.schedule.domain.repos.availability import AvailabilityRepo
from src.schedule.domain.repos.event import EventRepo
from src.schedule.domain.services.spots import SpotsService
from src.schedule.routes.v1.exceptions import AvailabilityNotFound, EventNotFound


class GetCalenderUsecase:
    def __init__(
        self,
        availability_repo: AvailabilityRepo,
        event_repo: EventRepo,
    ):
        self.availability_repo = availability_repo
        self.event_repo = event_repo

    def execute(
        self,
        event_id: UUID,
        start_date: date,
        end_date: date,
        timezone: str,
    ):
        event = self.event_repo.get(id=event_id)

        if not event:
            raise EventNotFound

        availability = self.availability_repo.get(id=event.availability_id)

        if not availability:
            raise AvailabilityNotFound

        service = SpotsService(availability, event)
        return service.generate_spots(start_date, end_date, timezone)
