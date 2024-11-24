from typing import List

from app.models.user_models import User
from app.deps import crud
from app.core.security import verify_password, decode_jwt


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
    fetched_user: User,
    plain_password: str
    ):
    """
    パスワード認証を実施後、ユーザーがアクティブであることを確認する。
    args:
        fetched_user: User
        plain_password: str
    return:
        True: 有効なユーザー
        False: 無効なユーザー(ログイン不可)
    """
    is_password_valid = verify_password(
        plain_password=plain_password,
        hashed_password=fetched_user.hashed_password
        )
    if not is_password_valid or not fetched_user.is_active:
        return False
    return True


