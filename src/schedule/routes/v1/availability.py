from fastapi import Response, status

from src.database import DBSessionDep
from src.schedule.data.repos.availability import AvailabilityRepoImpl
from src.schedule.domain.models.availability import Availability
from src.schedule.domain.schemas.availability import (
    SetAvailabilityResponseSchema,
    SetAvailabilitySchema,
)
from src.user.data.repos.user import UserRepoImpl
from src.main import app


@app.put(
    "/availability",
    status_code=status.HTTP_201_CREATED,
    response_model=SetAvailabilityResponseSchema,
)
def set_availability(
    payload: SetAvailabilitySchema,
    db_session: DBSessionDep,
    response: Response,
):
    repo = AvailabilityRepoImpl(db_session)
    user_repo = UserRepoImpl(db_session)
    # usecase = SetAvailabilityUsecase(repo)

    user = user_repo.get_by_email(payload.email)

    # Todo: handle the user not present case
    # Todo: send appropriate response if avail already exists

    if user:
        obj = Availability(user_id=user.id, **payload.model_dump(by_alias=True))
        availability = repo.insert(obj)
        return_payload = availability.model_dump()

    return return_payload
