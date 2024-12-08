from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import List
from uuid import UUID, uuid4


class UserBase(SQLModel):
    username: str = Field(max_length=50, min_length=3, index=True, unique=True)


class User(UserBase, table=True):
    uuid: UUID = Field(primary_key=True, index=True, unique=True, default=uuid4())
    create_at: datetime
    update_at: datetime
    hashed_password: str
    email: EmailStr = Field(index=True, unique=True)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)


class UserRegister(UserBase):
    email: EmailStr = Field(index=True, unique=True)
    password: str = Field(min_length=8, max_length=100)


class UserLogin(UserBase):
    password: str = Field(min_length=8, max_length=100)
