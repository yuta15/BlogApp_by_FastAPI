from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.core.security import decode_jwt
from app.deps.crud import SessionDeps
from app.deps.oauth import oauth2_scheme
from app.utils import crud, resolve
from app.models.user.article_models import Article, SchemaArticleInput, SchemaArticleOutput
from app.models.user.user_models import User


router = APIRouter(
    prefix='/article',
    tags=['article'],
    dependencies=[Depends(oauth2_scheme)]
)


def get_current_user(token: str = Depends(oauth2_scheme)):
    sub = decode_jwt(token)
    return sub
    

@router.post('/new')
async def new_article(
    session: SessionDeps,
    article: SchemaArticleInput,
    token: str = Depends(oauth2_scheme)
    ) -> SchemaArticleOutput:
    """
    記事を投稿するための関数
    """
    user: User = resolve.resolve_user_by_jwt(session=session, token=token)
    if user is None:
        raise HTTPException()
    created_article: Article = crud.create_article(session=session, input_article=article, user=user)
    return created_article


@router.get('/list')
async def article_list(session: SessionDeps,):
    articles: List[Article] = crud.fetch_articles(session=session)
    return articles

# 記事削除API
    # ユーザー識別の上、実施。
    # 記事のUUIDをユーザーに公表するか要件等
    # SuperUserはいつでも削除可能
    # @router.get('delete')
    # async def delete_article(
    #     session: SessionDeps,
    #     article: 
    # )


# 記事編集API
    # ユーザー識別の上実施可


# 記事リストを表示するAPI
    # その日にに投稿された記事を表示するAPI


