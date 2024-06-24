from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    email: EmailStr


class GetUserSchema(CreateUserSchema):
    id: UUID
