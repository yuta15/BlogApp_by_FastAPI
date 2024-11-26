from fastapi import HTTPException, Depends
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlmodel import Session

from app.deps.crud import SessionDeps, get_db
from app.models.user.article_models import Article


def insert_article(
    *,
    session: SessionDeps,
    article: Article
    ) -> None:
    """
    投稿された記事をinsertするための関数。
    
    args:
        session: SessionDeps,
        article: Article
        
    return:
        None
        
    Exception:
        HTTP_500_INTERNAL_SERVER_ERROR
    """
    print(article)
    try:
        session.add(article)
        session.commit()
        session.refresh(article)
    except Exception as e:
        print(e)
        raise e