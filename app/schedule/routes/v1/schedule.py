from fastapi import Response, status

from app.base.data.repos.sql_alchemy_unit_of_work import SQLAlchemyUnitOfWork
from app.schedule.data.repos.availability import AvailabilityRepoImpl
from app.schedule.domain.models.availability import Availability
from app.schedule.domain.schemas.availability import (
    SetAvailabilityResponseSchema,
    SetAvailabilitySchema,
)
from app.schedule.domain.schemas.schedule import CreateScheduleSchema
from app.schedule.domain.usecase.create_schedule import CreateScheduleUsecase
from app.user.data.repos.user import UserRepoImpl
from app.user.domain.models.user import User
from app.user.domain.schemas.user import CreateUserSchema, GetUserSchema
from app.user.domain.usecase.create_user import CreateUserUsecase
from app.main import app


@app.put(
    "/schedule",
    status_code=status.HTTP_201_CREATED,
    # response_model=SetAvailabilityResponseSchema,
)
def set_availability(
    payload: CreateScheduleSchema,
    response: Response,
):
    with SQLAlchemyUnitOfWork() as unit_of_work:
        availability_repo = AvailabilityRepoImpl(unit_of_work.session)
        availability = availability_repo.get(id=payload.availability_id)

        CreateScheduleUsecase()

    return {}
