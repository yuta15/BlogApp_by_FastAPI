from uuid import uuid4
from datetime import datetime

from app.core.setting import setting
from app.core.security import create_password_hash
from app.models.user.user_models import User, SchemaUserRegisterInput


def create_user_params(input_user: SchemaUserRegisterInput):
    """
    ユーザー作成用の情報を作成するための関数
    """
    user: User = User.model_validate(
        {
            "uuid": uuid4(),
            "username": input_user.username.encode('utf-8'),
            "email": input_user.email.encode('utf-8'),
            "create_at": datetime.now(setting.TZ),
            "update_at": datetime.now(setting.TZ),
            "hashed_password": create_password_hash(input_user.plain_password)
        }
    )
    return user

