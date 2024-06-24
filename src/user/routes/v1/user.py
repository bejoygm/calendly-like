from fastapi import status
from uuid import UUID

from src.main import app
from src.user.data.repos.user import UserRepoImpl
from src.user.domain.models.user import User
from src.user.domain.schemas.user import CreateUserSchema, GetUserSchema
from src.user.domain.usecase.create_user import CreateUserUsecase
from src.database import DBSessionDep
from src.user.routes.v1.exceptions import UserNotFound


@app.post(
    "/users",
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


@app.get(
    "/users/{user_id}",
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
