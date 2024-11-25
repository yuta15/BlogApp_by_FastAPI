from typing import List, Literal

from app.models.user.user_models import User
from app.models.superuser.superuser import Superuser
from app.deps.crud import SessionDeps
from app.utils import crud, resolve
from app.core.security import verify_password


def is_user_info_available(
    *, 
    table_model: Literal[User, Superuser],
    session: crud.SessionDeps, 
    **kwargs: dict,
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
    allowed_keys = ['uuid', 'username', 'email']
    dict_keys = kwargs.keys()
    bad_keys = [key for key in dict_keys if key in allowed_keys]
    if not bad_keys:
        return False
    
    users: List[table_model] = crud.fetch_users(
        session=session,
        table_model=table_model,
        condition='or',
        **kwargs,
    )
    return not bool(users)


def verify_user_credentials(
    fetched_user: User | Superuser,
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


