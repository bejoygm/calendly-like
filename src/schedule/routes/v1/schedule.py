from fastapi import APIRouter, Response, status

from src.database import DBSessionDep
from src.schedule.data.repos.availability import AvailabilityRepoImpl
from src.schedule.domain.schemas.schedule import CreateScheduleSchema

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
)


@router.put(
    "",
    status_code=status.HTTP_201_CREATED,
    # response_model=SetAvailabilityResponseSchema,
)
def set_availability(
    payload: CreateScheduleSchema,
    response: Response,
    db_session: DBSessionDep,
):
    availability_repo = AvailabilityRepoImpl(db_session)
    availability_repo.get(id=payload.availability_id)

    # CreateScheduleUsecase()

    return {}
