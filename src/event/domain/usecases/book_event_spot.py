from datetime import date
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import AwareDatetime

from src.event.domain.models.booking import Booking
from src.event.domain.repos.availability import AvailabilityRepo
from src.event.domain.repos.booking import BookingRepo
from src.event.domain.repos.event import EventRepo
from src.event.domain.services.email_service import send
from src.event.domain.services.spots import SpotsService
from src.event.routes.v1.exceptions import (
    AvailabilityNotFound,
    BookingNotAllowed,
    EventNotFound,
)


class BookEventSpotUsecase:
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
        spot: AwareDatetime,
        timezone: str,
        booked_by_id: UUID,
    ):
        event = self.event_repo.get(id=event_id)

        if not event:
            raise EventNotFound

        availability = self.availability_repo.get(id=event.availability_id)

        if not availability:
            raise AvailabilityNotFound

        service = SpotsService(availability, event)
        spot_date = spot.date()

        spots = service.generate_spots({}, spot_date, spot_date, timezone, booked_by_id)

        available = check_spot_availability(spot, spots)

        if not available:
            raise BookingNotAllowed

        # note: booking creation should be done under a serialized isolation level
        # if two or more parallel requests to different workers/nodes are made,
        # then this will end up creating duplicate bookings

        booking = Booking(
            booked_by_id=booked_by_id,
            booked_for_id=availability.user_id,
            spot=spot.astimezone(ZoneInfo("UTC")),
            timezone=timezone,
            event_id=event_id,
        )

        self.booking_repo.insert(booking)

        # hack: should be pushed off to a queue
        # send()

        return booking


def check_spot_availability(spot, spots):
    for day in spots["days"]:
        for s in day["spots"]:
            if s["start_time"] == spot:
                return True
    return False
