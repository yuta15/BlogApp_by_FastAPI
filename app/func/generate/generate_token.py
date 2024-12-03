from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import jwt


from app.core.setting import setting


def generate_token(payload: dict):
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

    token: str = jwt.encode(
        payload=payload,
        key=setting.SECRET_KEY,
        algorithm=setting.ALGORITHM
        )
    return token