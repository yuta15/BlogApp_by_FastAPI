from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from typing import List

from app.deps.crud import SessionDeps
from app.func.fetch import fetch_users
from app.models.superuser.superuser import Superuser


def fetch_superuser(
    *,
    session: SessionDeps,
    input_username: str,
    ) -> Superuser:
    """
    ユーザー名からユーザー情報を取得し、パスワード検証を実施する。
    問題なく完了すれば、ユーザー情報が取得される。
    """
    users: List[Superuser] = fetch_users.fetch_users(
        session=session,
        table_model=Superuser,
        username = input_username
    )
    if not users:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Bad Request')
    user: Superuser = users[0]
    return user