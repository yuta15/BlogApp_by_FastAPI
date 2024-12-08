from typing import List

from app.mods.user_mods.fetch.fetch_users import fetch_users
from app.deps.crud import SessionDeps
from app.models.User import UserRegister, User


def check_exist_user(*, session: SessionDeps, user_params:UserRegister):
    """
    ユーザーから送信されたデータが使用されていないことを確認する関数
    """
    users: List[User | None] = fetch_users(session=session, username=user_params.username, email=user_params.email)
    if users:
        return False
    return True