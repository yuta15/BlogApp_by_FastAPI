from uuid import uuid4
from datetime import datetime

from app.core.setting import setting
from app.models.user.user_models import User
from app.models.superuser.superuser import Superuser


def generate_user(
    **kwargs: dict
    ) -> User | Superuser:
    """
    DBへ投入可能なモデルを生成する。
    args:
        **kwargs:dict
            ユーザーの情報ユーザーから受け取った情報
            username: str
            
            hashed_password: str
                パスワード生成は、generate_hashed_password関数を使用して生成すること。
            
            email: EmailStr
            
            is_active: bool
                ユーザーを無効化したい場合はFalseを指定してください。
    return:
        user:User
            ユーザー情報
    """
    print()
    user: User = User.model_validate(
        {
            'uuid': uuid4(),
            'username': kwargs.get('username').encode('utf-8'),
            'email': kwargs.get('email').encode('utf-8'),
            'create_at': datetime.now(setting.TZ),
            'update_at': datetime.now(setting.TZ),
            'hashed_password': kwargs.get('hashed_password'),
            'is_active': kwargs.get('is_active', True)
        }
    )
    return user
