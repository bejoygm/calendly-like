from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class CreateUserSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    email: EmailStr


class GetUserSchema(CreateUserSchema):
    id: UUID
