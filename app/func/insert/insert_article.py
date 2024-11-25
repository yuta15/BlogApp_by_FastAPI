from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.deps.crud import SessionDeps
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
    try:
        session.add(article)
        session.commit()
        session.refresh(article)
    except:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Internal Server Error. Please try again later.'
            )