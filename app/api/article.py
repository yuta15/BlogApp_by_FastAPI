from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from uuid import UUID

from models.Article import PostedArticle, EditArticle, PublishArticle
from app.deps.crud import SessionDeps


router = APIRouter(
    prefix='/article2',
    tags=['article2'],
    dependencies=Depends()
)


@router.post('/post')
async def post(
    session: SessionDeps,
    article_params: PostedArticle
):
    """
    ArticleデータをPOSTするための関数
    """
    # Tokenチェック
    # POSTデータの生成
    # POSTデータのインサート処理
    # 結果をリターン
    

@router.get('/delete')
async def delete(
    session: SessionDeps,
    article_id: str
):
    """
    特定のarticleを削除するための関数
    """
    # tokenチェック
    # articleの削除
    # 結果をリターン
    
    
@router.post('/edit')
async def edit(
    session: SessionDeps,
    article_params: EditArticle
):
    """
    Articleの内容を編集するための関数
    """
    # Tokenチェック
    # Article情報をUpdate
    # 結果をリターン
    

@router.post('/publish')
async def publish(
    session: SessionDeps,
    article_params: PublishArticle
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
    article_id: UUID
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
    search_params: list
):
    """
    検索結果を返す関数
    """
    # Tokenチェック
    # Articleテーブルから検索結果を取得
    # 結果をリターン