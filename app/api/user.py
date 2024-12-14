from fastapi import APIRouter, Depends, HTTPException, Header, Response
from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from fastapi.security import OAuth2PasswordRequestForm

from app.models.User import UserRegister, User, UserLogin
from app.deps.crud import SessionDeps
from app.deps.oauth import resolve_user_from_token
from app.mods.user.user import (
    comfirm_not_exist_user, 
    generate_user,
    create_user,
    fetch_user_data,
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
    is_exist: bool = comfirm_not_exist_user(session=session, user_params=user_params)
    if is_exist is False:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail='Conflict User params')
    user: User | None = generate_user(user_params=user_params)
    if user is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Check Your Input Data')
    result: bool = create_user(session=session, user_params=user)
    if not result:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='Register Failed. Please Try again')
    else:
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
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Username or Password is Invalid')
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
    
    
@router.get('list', dependencies=Depends())
async def users(
    user_params: User = Depends(resolve_user_from_token),
    query: str = None,
):
    """
    ユーザー一覧を取得するための関数
    """
    
    # queryデータをもとに検索処理
    
    # 検索結果をリターン