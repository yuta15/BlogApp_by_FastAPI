from typing import List


from app.models.User import User, UserRegister

from app.mods.user_mods.fetch.fetch_users import fetch_users
from app.mods.user_mods.verify.verify_password import verify_password



def auth_user(*, session, user_params: UserRegister):
    """
    ユーザー認証を実施するための関数
    """
    
    users: List[User | None] = fetch_users(session=session, username=user_params.username)
    if not users:
        return False
    if users[0].is_active == False:
        return False
    is_available = verify_password(user_params.password, users[0].hashed_password)
    return is_available