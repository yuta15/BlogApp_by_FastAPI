from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.mods.user import fetch_user, create_token, auth_user
from app.deps.crud import SessionDeps
from app.models.user.user_models import User


router = APIRouter(
    prefix='/login',
    tags=['login']
)


@router.post('/')
async def login(
    session: SessionDeps, 
    form_input: Annotated[OAuth2PasswordRequestForm, Depends()], 
    ):
    """
    ログイン用API
    Formからユーザー名とパスワードを取得する。
    """
    user: User = fetch_user.fetch_user(
        session=session, 
        input_username=form_input.username
        )
    auth_user.auth_user(form_input.password, user=user)
    token:str = create_token.create_token(user=user)
    return {'access_token':token, 'token_type':"bearer"}
