from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Column


class ArticleBase(SQLModel):
    title: str = Field(max_length=150)
    


class Article(ArticleBase, table=True):
    id: UUID = Field(primary_key=True, index=True)
    body: str = Field(sa_column=Column(LONGTEXT))
    creaeted_at: datetime
    updated_at: datetime
    is_public: bool = Field(default=False)
    user_id: UUID = Field(foreign_key='user.uuid', index=True)


class SchemaArticleInput(ArticleBase):
    body: str


class SchemaArticleOutput(ArticleBase):
    body: str
    creaeted_at: datetime
    updated_at: datetime