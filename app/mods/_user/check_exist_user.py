from typing import List
from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT


from app.deps.crud import SessionDeps
from app.models.User import UserRegister, User
from app.func.fetch.fetch_users import fetch_users


def check_exist_user(
    *,
    session: SessionDeps,
    user_input: UserRegister
    ) -> None:
    """
    DB内の情報を確認し、ユーザー名、emailが重複しないことを確認する。
    args: 
        session: SessionDeps
        user_input: UserModel
        
    return:
        None

    """
    users: List[User] = fetch_users(
        session=session,
        table_model=User,
        condition='or',
        username=user_input.username.encode('utf-8'),
        email=user_input.email.encode('utf-8')
    )
    if not users:
        return True
    else:
        return False