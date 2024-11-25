from fastapi import Depends
from typing import Literal

from app.core.security import decode_jwt
from app.deps.oauth import oauth2_scheme
from app.deps.crud import SessionDeps
from app.utils import crud, verify
from app.models.user.user_models import User
from app.models.superuser.superuser import Superuser


def resolve_user_by_username(
    *,
    table_model: Literal[User, Superuser],
    session: SessionDeps,
    username: str
    ):
    users = crud.fetch_users(
        table_model=table_model, 
        session=session, 
        username=username
        )
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