from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import List
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Column
from uuid import UUID, uuid4


class ArticleBase(SQLModel):
    title: str = Field(max_length=150)
    
    
class Article(ArticleBase, table=True):
    id: UUID = Field(primary_key=True, index=True, default_factory=uuid4)
    body: str = Field(sa_column=Column(LONGTEXT))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_public: bool = Field(default=False)
    user_id: UUID = Field(foreign_key='user.uuid', index=True)


class CreateArticle(ArticleBase):
    body: str
    is_public: bool = Field(default=False)
    user_id: UUID
    
    
class ListArticle(ArticleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_public: bool
    user_id: UUID
    

class ArticleId(SQLModel):
    id: UUID