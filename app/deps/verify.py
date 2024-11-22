from fastapi import Depends, HTTPException
from typing import Union, List

from models.user_models import UserOutput, User, SchemaUserLoginInput
from deps import crud
from core.security import verify_password, decode_jwt


def is_user_info_available(
    *, 
    session: crud.SessionDeps, 
    username: str | None, 
    email: str | None
    ):
    """
    値が使用されていないことを確認する関数
    args: 
        session: SessionDeps
        username: str
        email: str
    return:
        ユーザー情報が使用されていない: True
        ユーザー情報が使用されている: False
    """
    users: List[User] = crud.fetch_users(
        session=session, 
        username=username, 
        email=email, 
        condition='or')
    return not bool(users)


def verify_user_credentials(
    input_user: SchemaUserLoginInput,
    fetched_user: User
    ):
    """
    ユーザーパスワード認証を行う。
    args:
        input_user: SchemaUserLoginInput
    return:
        bool
    """
    is_password_valid = verify_password(
        plain_password=input_user.plain_password,
        hashed_password=fetched_user.hashed_password
        )
    if not is_password_valid or not fetched_user.is_active:
        return False
    return True


