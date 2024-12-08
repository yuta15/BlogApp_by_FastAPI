from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.models.User import UserRegister, UserLogin, User
from app.deps.crud import SessionDeps
from app.deps.oauth import resolve_user_from_token
from app.mods.user_mods import (
    check_exist_user,
    generate_user,
    insert_user,
    auth_user,
    generate_token
)

router = APIRouter(
    prefix='/user2',
    tags=['user2']
)

@router.post('register')
async def register(
    session: SessionDeps,
    user_params:UserRegister
    ):
    """
    新規ユーザー登録用の関数
    """
    # 既存ユーザーの確認
    is_exist: bool = check_exist_user.check_exist_user(session=session, user_input=user_params)
    if not is_exist:
        HTTPException(status_code=HTTP_409_CONFLICT, detail='Conflict User params')
    # ユーザーデータの作成
    user: User | None = generate_user.generate_user(user_params=user_params)
    if user is None:
        HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Check Your Input Data')
    # ユーザーのinsert処理
    result: bool = insert_user.insert_user(session=session, user=user)
    if not result:
        HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='Register Failed. Please Try again')
    else:
        return {'detail': 'Successfull'}, 200


@router.post('/login')
async def login(
    session: SessionDeps,
    user_params: UserLogin, 
):
    """
    ユーザーログイン用の関数
    """
    # ユーザー名からユーザー情報を取得, ユーザーパスワードの認証
    is_available: bool = auth_user.auth_user(session=session, user_params=user_params)
    if not is_available:
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Please Check Your Input data')
    # Tokenを生成
    token: str = generate_token.generate_token(user_params)
    # Tokenをリターン
    return {'access_token':token, 'token_type':"bearer"}


@router.get('/logout', dependencies=Depends())
async def logout(
    session: SessionDeps,
    user_params: User = Depends(resolve_user_from_token)
):
    """
    ログアウト用関数
    """
    # Tokenチェック
    # ヘッダーからTokenを削除
    # ログアウト成功をリターン
    return {'access_token':'', 'token_type':''}
    
    
@router.get('list', dependencies=Depends())
async def users(
    session: SessionDeps,
    query: str = None
):
    """
    ユーザー一覧を取得するための関数
    """
    # Tokenチェック
    # queryデータをもとに検索処理
    # 検索結果をリターン