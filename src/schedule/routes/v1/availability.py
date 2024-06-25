from uuid import UUID
from fastapi import APIRouter, Response, status

from src.database import DBSessionDep
from src.schedule.data.repos.availability import AvailabilityRepoImpl
from src.schedule.domain.models.availability import Availability
from src.schedule.domain.schemas.availability import (
    AvailabilityRequestSchema,
    AvailabilityResponseSchema,
)
from src.schedule.domain.usecases.create_availablility import CreateAvailabilityUsecase
from src.schedule.routes.v1.exceptions import AvailabilityNotFound, UserNotFound
from src.user.data.repos.user import UserRepoImpl

router = APIRouter(
    prefix="/availability",
    tags=["availability"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AvailabilityResponseSchema,
)
def create_availability(
    payload: AvailabilityRequestSchema,
    db_session: DBSessionDep,
):
    user_repo = UserRepoImpl(db_session)
    user = user_repo.get_by_email(payload.email)

    if not user:
        raise UserNotFound

    repo = AvailabilityRepoImpl(db_session)
    usecase = CreateAvailabilityUsecase(availability_repo=repo)
    obj = Availability(user_id=user.id, **payload.model_dump(by_alias=True))
    availability = usecase.execute(obj)

    return availability.model_dump()


@router.get(
    "/{availability_id}",
    response_model=AvailabilityResponseSchema,
)
def get_availability(
    availability_id: UUID,
    db_session: DBSessionDep,
):
    repo = AvailabilityRepoImpl(db_session)
    availability = repo.get(availability_id)

    if not availability:
        raise AvailabilityNotFound

    return availability.model_dump()
