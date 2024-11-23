from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID


class ArticleBase(SQLModel):
    title: str = Field(max_length=150)
    body: str


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