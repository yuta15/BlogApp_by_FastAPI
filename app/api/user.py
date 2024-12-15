from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from fastapi.security import OAuth2PasswordRequestForm
import json
from pydantic import EmailStr
from uuid import UUID

from app.models.User import UserRegister, User, UserLogin
from app.deps.crud import SessionDeps
from app.deps.oauth import resolve_user_from_token
from app.mods.user.user import (
    check_duplicate_user_params, 
    generate_user,
    create_user,
    create_token,
    auth_user
    )

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/register')
async def register(
    session: SessionDeps,
    user_params:UserRegister
    ):
    """
    新規ユーザー登録用の関数
    """
    is_exist: bool = check_duplicate_user_params(session=session, user_params=user_params)
    if not is_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Conflict User params')
    user: User = generate_user(user_params=user_params)
    create_user(session=session, user_params=user)
    return {'detail': 'Successfull'}


@router.post('/login')
async def login(
    session: SessionDeps,
    form_input: OAuth2PasswordRequestForm = Depends()
):
    """
    ユーザーログイン用の関数
    """
    user_params: UserLogin = UserLogin.model_validate(
        {
            'username': form_input.username,
            'password': form_input.password
        }
    )
    is_auth, user = auth_user(session=session, user_params=user_params)
    if not is_auth:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username or Password is Invalid')
    token: str = create_token(user_params=user)
    return {'access_token':token, 'token_type':"bearer"}


@router.get('/logout')
async def logout(
    response: Response,
    user_params: User = Depends(resolve_user_from_token),
):
    """
    ログアウト用関数
    """
    response.headers['Authorization'] = ''
    return {'detail': 'logout successfully'}
    
    
@router.get('/list')
async def users(
    session: SessionDeps,
    username: str | None = None,
    email: EmailStr | None = None,
    uuid: UUID | None = None,
    args: str | None = Query(None)
):
    """
    ユーザー 一覧を取得するための関数
    """
    # if search_user:
    args = json.loads(args)
    
    return {
        'username': username,
        'email': email,
        'uuid': uuid,
        'args': args
        }
        
    # queryデータをもとに検索処理
    # users: List[User] = search_user(session=session, kwargs=query)
    # 検索結果をリターン