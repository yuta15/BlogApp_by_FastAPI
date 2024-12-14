from datetime import datetime

from app.core.setting import setting
from app.models.User import User


def generate_payload(
    user_params: User,
    ) -> dict:
    """
    payload生成用関数
    args:
        user_params: User | Superuser,
            JWTを作成するユーザーの情報
    return:
        payload: dict
            ユーザー情報から生成されたdict
    """
    
    payload = {
        'iat': datetime.now(setting.TZ),
        'exp': datetime.now(setting.TZ) + setting.EXPIRE_DELTA,
        'sub':{
            'username': user_params.username,
            'email': user_params.email
        }
    }
    
    return payload