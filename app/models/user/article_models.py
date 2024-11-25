from sqlmodel import SQLModel, Field, TEXT
from datetime import datetime
from uuid import UUID
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Column


class ArticleBase(SQLModel):
    title: str = Field(max_length=150)
    body: str = Field(sa_column=Column(LONGTEXT))


class Article(ArticleBase, table=True):
    id: UUID = Field(primary_key=True, index=True)
    creaeted_at: datetime
    updated_at: datetime
    is_public: bool = Field(default=False)
    user_id: UUID = Field(foreign_key='user.uuid', index=True)


class SchemaArticleInput(ArticleBase):
    pass


class SchemaArticleOutput(ArticleBase):
    creaeted_at: datetime
    updated_at: datetime