from fastapi import HTTPException
from datetime import datetime
from sqlmodel import select, or_
from typing import List, Literal
from uuid import UUID, uuid4
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.setting import setting
from app.models.user.user_models import User, SchemaUserRegisterInput
from app.models.user.article_models import Article, SchemaArticleInput
from app.models.superuser.superuser import Superuser, SuperuserInput
from app.deps.crud import SessionDeps


def create_user(
    *, 
    session: SessionDeps, 
    user_params: User | Superuser,
    ):
    """
    ユーザー作成
    """
    try:
        session.add(user_params)
        session.commit()
        session.refresh(user_params)
    except:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')


def fetch_users(
    *,
    session: SessionDeps,
    table_model: Literal[User, Superuser],
    condition: Literal['or', 'and'] = 'and',
    **kwargs: dict
    ):
    filters = []

    for column_name, field in kwargs.items():
        if column_name == 'uuid':
            filters.append(table_model.uuid == field)
        elif column_name == 'username':
            filters.append(table_model.username == field)
        elif column_name == 'email':
            filters.append(table_model.email == field)
        else:
            continue
    
    
    if not filters:
        stmt = select(table_model)
    elif condition == 'and':
        stmt = select(table_model).where(*filters)
    elif condition == 'or':
        stmt = select(table_model).where(or_(*filters)) 
    
    try:
        users: List[Literal[User, Superuser]] = session.exec(stmt).all()
    except:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    else:
        return users


def create_article(
    *, session: SessionDeps, 
    input_article: SchemaArticleInput, 
    user: User
    ):
    """
    新しい記事をDBへ保存するための関数
    """
    now = datetime.now(tz=setting.TZ)
    article: Article = Article.model_validate(input_article, update={
            'id': uuid4(),
            'creaeted_at': now,
            'updated_at': now,
            'user_id': user.uuid
        },
    )
    session.add(article)
    session.commit()
    session.refresh(article)
    return article


def fetch_articles(
    *,
    session: SessionDeps, 
    ):
    stmt = select(Article)
    articles: List[Article] = session.exec(stmt).all()
    return articles