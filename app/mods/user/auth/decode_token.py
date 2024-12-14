import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError, InvalidTokenError

from app.core.setting import setting


def decode_token(
    input_jwt: str
    ) -> dict: 
    """
    受信したTokenをデコードする。
    args:
        input_jwt: str
    return:
        subject: dict
    Exception:
        HTTP_401_UNAUTHORIZED
            expが超過した場合にraiseする。
        HTTP_500_INTERNAL_SERVER_ERROR
            その他エラーが発生した場合にraise
    """
    try:
        payload = jwt.decode(
            jwt=input_jwt, 
            key=setting.SECRET_KEY, 
            algorithms=setting.ALGORITHM
        )
    except (ExpiredSignatureError, InvalidSignatureError, DecodeError) as e:
        return None
    else:
        subject = payload.get('sub')
        return subject