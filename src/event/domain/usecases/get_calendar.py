from datetime import date
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import AwareDatetime

from src.event.domain.repos.availability import AvailabilityRepo
from src.event.domain.repos.booking import BookingRepo
from src.event.domain.repos.event import EventRepo
from src.event.domain.services.spots import SpotsService
from src.event.routes.v1.exceptions import AvailabilityNotFound, EventNotFound


class GetCalenderUsecase:
    def __init__(
        self,
        availability_repo: AvailabilityRepo,
        event_repo: EventRepo,
        booking_repo: BookingRepo,
    ):
        self.availability_repo = availability_repo
        self.event_repo = event_repo
        self.booking_repo = booking_repo

    def execute(
        self,
        event_id: UUID,
        user_id: UUID,
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

        # get bookings of the query user and event creqtor
        bookings = self.booking_repo.filter_by_user_id(user_id)
        event_creator_bookings = self.booking_repo.filter_by_user_id(
            availability.user_id
        )

        # convert all bookings to query user's timezone for easy lookup
        booked_spots_dict: dict[AwareDatetime, bool] = {}
        for b in bookings:
            booked_spots_dict[b.spot] = True
        for b in event_creator_bookings:
            converted = b.spot.astimezone(ZoneInfo(timezone))
            booked_spots_dict[converted] = True

        service = SpotsService(availability, event)
        return service.generate_spots(
            booked_spots_dict, start_date, end_date, timezone, user_id
        )
