from datetime import datetime
from pydantic import EmailStr, BaseModel
from uuid import UUID
from sqlmodel import SQLModel, Field


class UserModel(SQLModel):
    username: str = Field(max_length=50, min_length=3, index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    

class User(UserModel, table=True):
    uuid: UUID = Field(primary_key=True, index=True, unique=True)
    create_at: datetime
    update_at: datetime
    hashed_password: str
    is_active: bool = Field(default=True)


class UserOutput(UserModel):
    uuid: UUID
    create_at: datetime
    update_at: datetime
    
    class Config:
        orm_mode = True


class SchemaUserBase(BaseModel):
    username: str = Field(max_length=50, min_length=3)


class SchemaUserRegisterInput(SchemaUserBase):
    email: EmailStr
    plain_password: str = Field(min_length=8, max_length=100)


class SchemaUserRegisterOutput(SchemaUserBase):
    email: EmailStr
    create_at: datetime
    update_at: datetime
