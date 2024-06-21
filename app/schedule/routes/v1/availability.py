from fastapi import Response, status

from app.base.data.repos.sql_alchemy_unit_of_work import SQLAlchemyUnitOfWork
from app.schedule.data.repos.availability import AvailabilityRepoImpl
from app.schedule.domain.models.availability import Availability
from app.schedule.domain.schemas.availability import (
    SetAvailabilityResponseSchema,
    SetAvailabilitySchema,
)
from app.user.data.repos.user import UserRepoImpl
from app.user.domain.models.user import User
from app.user.domain.schemas.user import CreateUserSchema, GetUserSchema
from app.user.domain.usecase.create_user import CreateUserUsecase
from app.main import app


@app.put(
    "/availability",
    status_code=status.HTTP_201_CREATED,
    response_model=SetAvailabilityResponseSchema,
)
def set_availability(
    payload: SetAvailabilitySchema,
    response: Response,
):
    with SQLAlchemyUnitOfWork() as unit_of_work:
        repo = AvailabilityRepoImpl(unit_of_work.session)
        user_repo = UserRepoImpl(unit_of_work.session)
        # usecase = SetAvailabilityUsecase(repo)

        user = user_repo.get_by_email(payload.email)

        # Todo: handle the user not present case
        # Todo: send appropriate response if avail already exists

        if user:
            obj = Availability(user_id=user.id, **payload.model_dump(by_alias=True))
            availability = repo.insert(obj)
            unit_of_work.commit()
            return_payload = availability.model_dump()

    return return_payload
