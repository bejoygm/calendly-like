from datetime import date
from uuid import UUID

from fastapi import APIRouter, Query, status

from src.database import DBSessionDep
from src.schedule.data.repos.availability import AvailabilityRepoImpl
from src.schedule.data.repos.event import EventRepoImpl
from src.schedule.domain.models.event import Event
from src.schedule.domain.schemas.event import (
    CreateEventResponseSchema,
    CreateEventSchema,
    GetEventCalendar,
)
from src.schedule.domain.usecase.get_calendar import CreateCalenderUsecase
from src.schedule.routes.v1.exceptions import AvailabilityNotFound

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
    timezone: str,
    start_date: date = Query(..., description="eg: 2024-06-25"),
    end_date: date = Query(..., description="eg: 2024-06-26"),
):
    event_repo = EventRepoImpl(db_session)
    availability_repo = AvailabilityRepoImpl(db_session)

    usecase = CreateCalenderUsecase(
        availability_repo=availability_repo,
        event_repo=event_repo,
    )

    calender_events = usecase.execute(
        event_id=event_id,
        start_date=start_date,
        end_date=end_date,
        timezone=timezone,
    )

    return_payload = calender_events
    return return_payload
