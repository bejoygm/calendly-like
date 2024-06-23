from fastapi import status

from app.user.data.repos.user import UserRepoImpl
from app.user.domain.models.user import User
from app.user.domain.schemas.user import CreateUserSchema, GetUserSchema
from app.user.domain.usecase.create_user import CreateUserUsecase
from app.main import app
from app.di import DBSessionDep


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=GetUserSchema,
)
async def create_user(
    payload: CreateUserSchema,
    db_session: DBSessionDep,
):
    repo = UserRepoImpl(db_session)
    usecase = CreateUserUsecase(repo)
    user = usecase.execute(User(**payload.model_dump()))
    await db_session.commit()
    return_payload = user.model_dump()
    return return_payload
