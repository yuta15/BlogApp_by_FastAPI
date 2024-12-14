from fastapi.security import OAuth2PasswordBearer 

from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlmodel import Session
from typing import List

from app.deps.crud import get_db
from app.mods.user_mods.auth import decode_token
from app.mods.user_mods.db import fetch_users
from app.models.User import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def resolve_user_from_token(
    *,
    session: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
    ) -> User:
    """
    Token情報からToken情報を取得する。
    """
    subject = decode_token.decode_token(token)
    users: List[User] = fetch_users.fetch_users(session=session, username=subject.get('username'))
    


    if not users:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    
    return users[0]


# def auth_from_token(
    
# )