from datetime import datetime

from app.mods.user_mods.sanitize import sanitize_to_utf8
from app.mods.user_mods.generate import generate_hashed_password
from app.models.User import User, UserRegister
from app.core.setting import setting


def generate_user(user_params: UserRegister):
    """
    Insert可能なデータを生成するための関数
    """
    sanitized_params:dict = sanitize_to_utf8.sanitize_to_utf8(**user_params)
    hashed_password: str = generate_hashed_password.generate_hash_password(user_params.password)
    current_time = datetime.now(setting.TZ)
    try:
        user: User = User.model_validate(
            {
                'username': sanitized_params.get('username'),
                'email': sanitized_params.get('email'),
                'create_at': current_time,
                'update_at': current_time,
                'hashed_password': hashed_password,
                'is_active': True,
                'is_admin': False
            },
        )
    except ValueError:
        return None
    else:
        return user