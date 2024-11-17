from datetime import datetime
from pydantic import Field, EmailStr, BaseModel
from typing import Union
from uuid import UUID


class SchemaUserBase(BaseModel):
    username: str = Field(max_length=50, min_length=3)
    email: EmailStr


class SchemaUserRegisterInput(SchemaUserBase):
    plain_password: str = Field(min_length=8, max_length=100)


class SchemaUserRegisterOutput(SchemaUserBase):
    create_at: datetime
    update_at: datetime
    
    
class SchemaUserReference(BaseModel):
    username: Union[str, None]
    email: Union[str, None]



