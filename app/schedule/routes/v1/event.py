from datetime import date
from uuid import UUID
from fastapi import Response, status

from app.base.data.repos.sql_alchemy_unit_of_work import SQLAlchemyUnitOfWork
from app.schedule.data.repos.availability import AvailabilityRepoImpl
from app.schedule.data.repos.event import EventRepoImpl
from app.schedule.domain.models.availability import Availability
from app.schedule.domain.schemas.availability import (
    SetAvailabilityResponseSchema,
    SetAvailabilitySchema,
)
from app.schedule.domain.schemas.event import (
    CreateEventResponseSchema,
    CreateEventSchema,
    GetEventCalendar,
)
from app.schedule.domain.models.event import Event
from app.main import app
from app.schedule.domain.usecase.get_calendar import CreateCalenderUsecase


@app.post(
    "/event",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateEventResponseSchema,
)
def set_availability(
    payload: CreateEventSchema,
):
    with SQLAlchemyUnitOfWork() as unit_of_work:
        repo = EventRepoImpl(unit_of_work.session)
        obj = Event(**payload.model_dump())
        event = repo.insert(obj)
        unit_of_work.commit()
        return_payload = event.model_dump()
    return return_payload


@app.get(
    "/get/{event_id}/calendar",
    response_model=GetEventCalendar,
)
def get_event_calendar(
    event_id: UUID,
    start_date: date,
    end_date: date,
    timezone: str,
):
    with SQLAlchemyUnitOfWork() as unit_of_work:
        event_repo = EventRepoImpl(unit_of_work.session)
        availability_repo = AvailabilityRepoImpl(unit_of_work.session)

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
