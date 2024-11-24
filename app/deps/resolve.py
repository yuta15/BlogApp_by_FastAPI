from typing import Annotated
from fastapi import Depends

from app.deps.oauth import oauth2_scheme
from app.core.security import decode_jwt
from app.deps.crud import fetch_users, SessionDeps


def resolve_user_by_username(
    *, 
    session: SessionDeps,
    username: str
    ):
    users = fetch_users(session=session, username=username)
    if not users or len(users) > 1:
        return None
    return users[0]


def resolve_user_by_jwt(
    *, 
    session: SessionDeps,
    token: str = Depends(oauth2_scheme)):
    """
    JWTの情報からユーザー情報を取得する処理
    """
    subject = decode_jwt(input_jwt=token).get('sub')
    user = resolve_user_by_username(session=session, username=subject.get('username'))
    return user