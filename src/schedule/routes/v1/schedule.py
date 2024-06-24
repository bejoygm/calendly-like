from fastapi import Response, status

from src.database import DBSessionDep
from src.schedule.data.repos.availability import AvailabilityRepoImpl
from src.schedule.domain.models.availability import Availability
from src.schedule.domain.schemas.availability import (
    SetAvailabilityResponseSchema,
    SetAvailabilitySchema,
)
from src.schedule.domain.schemas.schedule import CreateScheduleSchema
from src.schedule.domain.usecase.create_schedule import CreateScheduleUsecase
from src.main import app


@app.put(
    "/schedule",
    status_code=status.HTTP_201_CREATED,
    # response_model=SetAvailabilityResponseSchema,
)
def set_availability(
    payload: CreateScheduleSchema,
    response: Response,
    db_session: DBSessionDep,
):
    availability_repo = AvailabilityRepoImpl(db_session)
    availability = availability_repo.get(id=payload.availability_id)

    # CreateScheduleUsecase()

    return {}
