import jwt

from app.core.setting import setting
from app.mods.user_mods.fetch.fetch_users import fetch_users
from app.mods.user_mods.generate.generate_payload import generate_payload
from app.models.User import UserLogin, User


def generate_token(*, session, user_params: UserLogin):
    """
    JWT生成用関数
    args:
        Tokenに含めるPayload
        payload: dict
        
    return:
        token: str
            生成されたToken
            
    Exception
    """
    user: User = fetch_users(session=session, username=user_params.username)[0]
    payload = generate_payload(user_params=user)
    token: str = jwt.encode(
        payload=payload,
        key=setting.SECRET_KEY,
        algorithm=setting.ALGORITHM
        )
    return token