from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from typing import List

from app.deps.crud import SessionDeps
from app.func.fetch import fetch_users
from app.func.check import check_password
from app.models.User import User


def fetch_user(
    *,
    session: SessionDeps,
    input_username: str,
    ) -> User:
    """
    ユーザー名からユーザー情報を取得し、パスワード検証を実施する。
    問題なく完了すれば、ユーザー情報が取得される。
    """
    users: List[User] = fetch_users.fetch_users(
        session=session,
        table_model=User,
        username = input_username
    )
    if not users:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Bad Request')
    user: User = users[0]
    return user