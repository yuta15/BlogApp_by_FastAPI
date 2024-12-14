from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlmodel import Session
from typing import List

from app.deps.oauth import oauth2_scheme
from app.deps.crud import SessionDeps, get_db
from app.func.check import check_token
from app.func.fetch import fetch_users
from app.models.User import User


def resolve_user_from_token(
    *,
    session: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
    ) -> User:
    """
    Token情報からToken情報を取得する。
    """
    subject = check_token.check_token(token)
    users: List[User] = fetch_users.fetch_users(
        session=session,
        table_model=User,
        username=subject.get('username')
    )
    if not users:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    
    return users[0]