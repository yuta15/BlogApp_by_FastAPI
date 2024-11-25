from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import jwt

from core.setting import setting


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
    try:
        token: str = jwt.encode(
            payload=payload,
            key=setting.SECRET_KEY,
            algorithm=setting.ALGORITHM
            )
    except:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Internal Server Error. Please try again later.'
            )
    else:
        return token