import base64
from datetime import date, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import AwareDatetime
from ics import Calendar, Event
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
    UserNotFound,
)
from src.user.domain.models.user import User
from src.user.domain.repos.user import UserRepo


class BookEventSpotUsecase:
    def __init__(
        self,
        availability_repo: AvailabilityRepo,
        event_repo: EventRepo,
        booking_repo: BookingRepo,
        user_repo: UserRepo,
    ):
        self.availability_repo = availability_repo
        self.event_repo = event_repo
        self.booking_repo = booking_repo
        self.user_repo = user_repo

    def execute(
        self,
        event_id: UUID,
        spot: AwareDatetime,
        timezone: str,
        booked_by_id: UUID,
    ):
        booking_user = self.user_repo.get(booked_by_id)
        if not booking_user:
            raise UserNotFound

        event = self.event_repo.get(id=event_id)

        if not event:
            raise EventNotFound

        availability = self.availability_repo.get(id=event.availability_id)

        if not availability:
            raise AvailabilityNotFound

        event_user = self.user_repo.get(availability.user_id)
        if not event_user:
            raise UserNotFound

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

        # hack: this is a sync call
        # ideally it should be pushed off to a queue with idempotency support
        send_invites(event, booking, booking_user, event_user)

        return booking


def check_spot_availability(spot, spots):
    for day in spots["days"]:
        for s in day["spots"]:
            if s["start_time"] == spot:
                return True
    return False


def send_invites(event: Event, booking: Booking, booking_user: User, event_user: User):
    ics = generate_ics(event, booking)
    booking_subject = f"You are invited for {event.name}"
    content = f"Meeting details\n{event.description}"
    send(ics, booking_user.email, booking_subject, content)

    event_subject = f"{booking_user.name} blocked your calendar"
    send(ics, event_user.email, event_subject, content)


def generate_ics(event: Event, booking: Booking):
    c = Calendar()
    e = Event()
    e.name = event.name
    e.summary = event.name
    e.description = event.description
    e.begin = booking.spot
    e.end = booking.spot + timedelta(minutes=event.duration)
    c.events.add(e)

    ics = c.serialize()
    return base64.b64encode(ics.encode()).decode()
