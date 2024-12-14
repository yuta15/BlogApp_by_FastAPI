from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from uuid import UUID
from starlette.status import HTTP_400_BAD_REQUEST, 

from app.models.User import User
from app.models.Article import PostedArticle, EditArticle, PublishArticle
from app.deps.crud import SessionDeps
from app.deps.oauth import resolve_user_from_token


router = APIRouter(
    prefix='/article2',
    tags=['article2'],
    dependencies=Depends()
)


@router.post('/post')
async def post(
    session: SessionDeps,
    article_params: PostedArticle,
    user_params: User = Depends(resolve_user_from_token)
):
    """
    ArticleデータをPOSTするための関数
    """
    # POSTデータの生成
    post_data = generate_post_data(article_params, user_params)
    # POSTデータのインサート処理
    is_result = insert_post(post_data)
    # 結果をリターン
    if is_result:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Failed: Can not save the post Data')
    return {'detail': 'Success!'}


@router.get('/delete')
async def delete(
    session: SessionDeps,
    article_id: str,
    user_params: User = Depends(resolve_user_from_token)
):
    """
    特定のarticleを削除するための関数
    """
    # articleの存在チェック
    is_exist = bool(fetch_article(article_id))
    if is_exist:
        HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Do not find the article')
    # articleの削除
    is_result = delete_article(article_id)
    if not is_result:
        HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Failed: Article can not be deleted')
    # 結果をリターン
    return {'detail': 'Success: Article is Deleted'}
    
    
@router.post('/edit')
async def edit(
    session: SessionDeps,
    article_params: EditArticle,
    user_params: User = Depends(resolve_user_from_token)
):
    """
    Articleの内容を編集するための関数
    """
    # Article情報を取得
    article = fetch_article(article_params.id)
    new_article = edit_article(article, article_params)
    is_result = update_article(new_article)
    if not is_result:
        HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Update failed')
    # 結果をリターン
    return {'detail': 'Update Successfully'}


@router.post('/publish')
async def publish(
    session: SessionDeps,
    article_params: PublishArticle,
    user_params: User = Depends(resolve_user_from_token)
):
    """
    Articleの公開、非公開を設定するための関数
    """
    # Tokenチェック
    # Article情報をUpdate
    # 結果をリターン
    
    
@router.get('/list')
async def article_list(
    session: SessionDeps,
    start_num: int = 0,
    end_num: int = 100,
    user_params: User = Depends(resolve_user_from_token)
):
    """
    Article一覧を取得する関数
    """
    # Tokenチェック
    # Articleの一覧を取得　※デフォルトでは0~100の新しいデータを取得する。
    # 結果をリターン
    

@router.get('/{article_id}')
async def article(
    session: SessionDeps,
    article_id: UUID,
    user_params: User = Depends(resolve_user_from_token)
):
    """
    特定の記事のデータを取得する関数
    """
    # Tokenチェック
    # Articleデータを取得
    # 結果をリターン


@router.get('/search')
async def search(
    session: SessionDeps,
    search_params: list,
    user_params: User = Depends(resolve_user_from_token)
):
    """
    検索結果を返す関数
    """
    # Tokenチェック
    # Articleテーブルから検索結果を取得
    # 結果をリターン