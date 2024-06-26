from uuid import UUID

from fastapi import APIRouter, status

from src.database import DBSessionDep
from src.user.data.repos.user import UserRepoImpl
from src.user.domain.models.user import User
from src.user.domain.schemas.user import CreateUserSchema, GetUserSchema
from src.user.domain.usecases.create_user import CreateUserUsecase
from src.user.routes.v1.exceptions import UserNotFound

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=GetUserSchema,
)
def create_user(
    payload: CreateUserSchema,
    db_session: DBSessionDep,
):
    repo = UserRepoImpl(db_session)
    usecase = CreateUserUsecase(repo)
    user = usecase.execute(User(**payload.model_dump()))
    return_payload = user.model_dump()
    return return_payload


@router.get(
    "/{user_id}",
    response_model=GetUserSchema,
)
def get_user(
    user_id: UUID,
    db_session: DBSessionDep,
):
    repo = UserRepoImpl(db_session)
    user = repo.get(user_id)
    if not user:
        raise UserNotFound
    return user.model_dump()
