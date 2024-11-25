from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
import jwt
from jwt.exceptions import ExpiredSignatureError

from app.core.setting import setting


def check_token(
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
        decoded_token = jwt.decode(
            jwt=input_jwt, 
            key=setting.SECRET_KEY, 
            algorithms=setting.ALGORITHM
        )
    except ExpiredSignatureError:
        HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Unauthorized User')
    except:
        HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error. Please try again later.')
    else:
        subject = decoded_token.get('subject')
        return subject