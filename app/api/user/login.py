from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Annotated

from app.core.security import generate_token
from app.deps.crud import SessionDeps
from app.utils.verify import verify_user_credentials
from app.utils.resolve import resolve_user_by_username
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
    """
    user: User = resolve_user_by_username(session=session, username=form_input.username)
    if user is None:
        raise HTTPException(status_code=401, detail='Unauthorization Error')
    
    is_auth: bool = verify_user_credentials(
        fetched_user=user,
        plain_password=form_input.password
        )
    if not is_auth:
        raise HTTPException(status_code=401, detail='Unauthorization Error')

    token = generate_token(username=user.username, email=user.email)
    
    return {"access_token": token, "token_type": "bearer"}