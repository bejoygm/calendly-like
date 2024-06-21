from fastapi import status

from app.base.data.repos.sql_alchemy_unit_of_work import SQLAlchemyUnitOfWork
from app.user.data.repos.user import UserRepoImpl
from app.user.domain.models.user import User
from app.user.domain.schemas.user import CreateUserSchema, GetUserSchema
from app.user.domain.usecase.create_user import CreateUserUsecase
from app.main import app


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=GetUserSchema,
)
def create_user(payload: CreateUserSchema):
    with SQLAlchemyUnitOfWork() as unit_of_work:
        repo = UserRepoImpl(unit_of_work.session)
        usecase = CreateUserUsecase(repo)
        user = usecase.execute(User(**payload.model_dump()))
        unit_of_work.commit()
        return_payload = user.model_dump()
    return return_payload
