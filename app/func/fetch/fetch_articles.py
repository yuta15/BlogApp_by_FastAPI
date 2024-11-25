from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlmodel import select, or_
from typing import Literal, List

from app.deps.crud import SessionDeps
from app.models.user.article_models import Article


def fetch_articles(
    *,
    session: SessionDeps,
    condition: Literal['or', 'and'] = 'and',
    **kwargs: dict
) -> List[Article | None]:
    """
    一致する記事情報を取得するための関数
    
    args:
        session: SessionDeps
        table_model: Literal[User, Superuser]
            取得したテーブルごとに、User, Superuserを指定する。
            
        condition: Literal['or', 'and'] = 'and',
            kwargs内の情報をor検索もしくはand検索を指定する。
            デフォルトはand
        
        **kwargs: dict
            検索に必要な情報を指定する。
            指定可能なキー値は、title, user_id, body
            
            
    return:
        articles: List[Article | None]
            Article情報のリストもしくは[]が応答される。
    
    Exception:
        何らかの影響でサーバーから正常に応答がない場合は、HTTP_500_INTERNAL_SERVER_ERRORを返す。
    """

    filters = []
    
    """
    記事情報を取得するための処理を記述予定。
    title, body内検索文字列を含むものの検索を行う。
    もしくは特定のuser_idを持つ記事を検索等。
    """
    
    
    # try:
    #     users: List[Article] | None = session.exec(stmt).all()
    # except:
    #     raise HTTPException(
    #         status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
    #         detail='Internal Server Error. Please try again later.'
    #     )
    # else:
    #     return users