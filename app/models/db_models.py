
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from uuid import UUID


class UserModel(SQLModel):
    username: str = Field(max_length=50, min_length=3, index=True)
    email: EmailStr
    

class User(UserModel, table=True):
    uuid: UUID = Field(primary_key=True, index=True)
    create_at: datetime
    update_at: datetime
    hashed_password: str


class UserOutput(UserModel):
    uuid: UUID
    create_at: datetime
    update_at: datetime
    
    class Config:
        orm_mode = True

    
class UserVerify(UserModel):
    pass