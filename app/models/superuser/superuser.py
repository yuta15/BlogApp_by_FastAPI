from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime
from uuid import UUID


class SuperuserBase(SQLModel):
    username: str = Field(max_length=50, min_length=3, index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)


class Superuser(SuperuserBase, table=True):
    uuid: UUID = Field(primary_key=True, index=True, unique=True)
    create_at: datetime
    update_at: datetime
    hashed_password: str
    is_active: bool = Field(default=True)


class SuperuserInput(SuperuserBase):
    password: str = Field(min_length=8, max_length=50)