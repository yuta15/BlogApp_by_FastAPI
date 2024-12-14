from fastapi import Depends
from sqlmodel import Session

from app.models.user.article_models import SchemaArticleInput, Article
from app.models.user.user_models import User
from app.deps.crud import SessionDeps, get_db
from app.func.generate import generate_article_data
from app.func.insert import insert_article


def create_new_article(
    *,
    session: SessionDeps,
    article: SchemaArticleInput,
    user: User
    ):
    """
    記事を作成するための処理。
    insertまで実施する。
    """
    
    article: Article = generate_article_data.generate_article_data(
        title=article.title,
        body=article.body,
        user_id=user.uuid,
        )
    insert_article.insert_article(session=session, article=article)