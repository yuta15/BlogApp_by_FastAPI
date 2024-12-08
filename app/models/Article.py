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
    id: UUID = Field(primary_key=True, index=True)
    body: str = Field(sa_column=Column(LONGTEXT))
    creaeted_at: datetime
    updated_at: datetime
    is_public: bool = Field(default=False)
    user_id: UUID = Field(foreign_key='user.uuid', index=True)
    comments: List[UUID | None] = Field(foreign_key='comment.uuid', index=True, default=[])


class PostedArticle(ArticleBase):
    body: str = Field(sa_column=Column(LONGTEXT))
    
    
class EditArticle(ArticleBase):
    id: UUID = Field(primary_key=True, index=True)
    title: str = Field(max_length=150)
    body: str = Field(sa_column=Column(LONGTEXT))
    
    
class PublishArticle(ArticleBase):
    id: UUID = Field(primary_key=True, index=True)
    is_publish = Field(default=False)
