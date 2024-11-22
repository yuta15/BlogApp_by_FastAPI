from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List

from models.user_models import SchemaUserLoginInput, ShemaUserLoginOutput, User
from deps.crud import SessionDeps, fetch_users
from deps.verify import verify_user_credentials
from core.security import decode_jwt, generate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
router = APIRouter(
    prefix='/login',
    tags=['login']
)


@router.post('/')
async def login(
    session: SessionDeps, 
    login_user_input: SchemaUserLoginInput, 
    ):
    """
    ログイン用API
    """
    users: List[User] = fetch_users(session=session, username=login_user_input.username)
    if not users or len(users) > 1:
        raise HTTPException(status_code=401, detail='Unauthorization Error')
    user: User = users[0]
    is_auth: bool = verify_user_credentials(
        input_user=login_user_input,
        fetched_user=user
        )
    if not is_auth:
        raise HTTPException(status_code=401, detail='Unauthorization Error')

    token = generate_token(username=user.username, email=user.email)
    return {"access_token": token, "token_type": "bearer"}
