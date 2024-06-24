from datetime import date
from uuid import UUID
from fastapi import status

from src.database import DBSessionDep
from src.schedule.data.repos.availability import AvailabilityRepoImpl
from src.schedule.data.repos.event import EventRepoImpl
from src.schedule.domain.schemas.event import (
    CreateEventResponseSchema,
    CreateEventSchema,
    GetEventCalendar,
)
from src.schedule.domain.models.event import Event
from src.main import app
from src.schedule.domain.usecase.get_calendar import CreateCalenderUsecase


@app.post(
    "/event",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateEventResponseSchema,
)
def set_availability(
    payload: CreateEventSchema,
    db_session: DBSessionDep,
):
    repo = EventRepoImpl(db_session)
    obj = Event(**payload.model_dump())
    event = repo.insert(obj)
    return_payload = event.model_dump()
    return return_payload


@app.get(
    "/get/{event_id}/calendar",
    response_model=GetEventCalendar,
)
def get_event_calendar(
    db_session: DBSessionDep,
    event_id: UUID,
    start_date: date,
    end_date: date,
    timezone: str,
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
