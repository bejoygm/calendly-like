from datetime import date, datetime
from uuid import UUID

from fastapi import APIRouter, Query, status

from src.database import DBSessionDep
from src.event.data.repos.availability import AvailabilityRepoImpl
from src.event.data.repos.booking import BookingRepoImpl
from src.event.data.repos.event import EventRepoImpl
from src.event.domain.models.event import Event
from src.event.domain.schemas.event import (
    BookEventSpotRequestSchema,
    BookEventSpotResponseSchema,
    CreateEventResponseSchema,
    CreateEventSchema,
    GetEventCalendar,
)
from src.event.domain.usecases.get_calendar import GetCalenderUsecase
from src.event.domain.usecases.book_event_spot import BookEventSpotUsecase
from src.event.routes.v1.exceptions import AvailabilityNotFound
from src.user.data.repos.user import UserRepoImpl

router = APIRouter(
    prefix="/events",
    tags=["events"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateEventResponseSchema,
)
def create_event(
    payload: CreateEventSchema,
    db_session: DBSessionDep,
):
    availability_repo = AvailabilityRepoImpl(db_session)
    availability = availability_repo.get(payload.availability_id)

    if not availability:
        raise AvailabilityNotFound

    repo = EventRepoImpl(db_session)
    obj = Event(**payload.model_dump())
    event = repo.insert(obj)
    return_payload = event.model_dump()
    return return_payload


@router.get(
    "/{event_id}/calendar",
    response_model=GetEventCalendar,
)
def get_event_calendar(
    db_session: DBSessionDep,
    event_id: UUID,
    user_id: UUID,
    timezone: str,
    start_date: date = Query(..., description="eg: 2024-06-25"),
    end_date: date = Query(..., description="eg: 2024-06-26"),
):
    event_repo = EventRepoImpl(db_session)
    availability_repo = AvailabilityRepoImpl(db_session)
    booking_repo = BookingRepoImpl(db_session)

    usecase = GetCalenderUsecase(
        availability_repo=availability_repo,
        event_repo=event_repo,
        booking_repo=booking_repo,
    )

    calender_events = usecase.execute(
        event_id=event_id,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        timezone=timezone,
    )

    return calender_events


@router.post(
    "/{event_id}/book",
    response_model=BookEventSpotResponseSchema,
)
def book_event_spot(
    db_session: DBSessionDep,
    event_id: UUID,
    payload: BookEventSpotRequestSchema,
):
    availability_repo = AvailabilityRepoImpl(db_session)
    event_repo = EventRepoImpl(db_session)
    booking_repo = BookingRepoImpl(db_session)
    user_repo = UserRepoImpl(db_session)

    usecase = BookEventSpotUsecase(
        availability_repo,
        event_repo,
        booking_repo,
        user_repo,
    )
    response = usecase.execute(
        event_id,
        spot=payload.spot,
        timezone=payload.timezone,
        booked_by_id=payload.user_id,
    )
    return response
