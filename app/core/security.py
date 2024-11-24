from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from pydantic import EmailStr

from app.core.setting import setting


PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = setting.ALGORITHM
SECRET_KEY = setting.SECRET_KEY
CURRENT_TIME = datetime.now(setting.TZ)
EXPIRE_DELTA = setting.EXPIRE_DELTA

def create_password_hash(password: str):
    """
    パスワードをハッシュ化する関数
    """
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    パスワード検証用関数
    args: 
        plain_password: str
        hashed_password: str
    return:
        True: 検証に成功した場合
        False: 検証に失敗した場合
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def generate_token(username: str, email: EmailStr):
    """
    JWT生成用関数
    args:
        username: str
        email: EmailStr
    return:
        encoded_jwt: str
    """
    global ALGORITHM, SECRET_KEY, CURRENT_TIME, EXPIRE_DELTA
    payload = {
        'iat': CURRENT_TIME,
        'exp': CURRENT_TIME + EXPIRE_DELTA,
        'sub': {
            'username': username,
            'email': email
        }
    }
    encoded_jwt: str = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
        )
    return encoded_jwt


def decode_jwt(input_jwt: jwt):
    """
    JWTの検証用関数
    """
    global ALGORITHM, SECRET_KEY, CURRENT_TIME
    
    try:
        decoded_jwt = jwt.decode(
            jwt=input_jwt, 
            key=SECRET_KEY, 
            algorithms=[ALGORITHM]
            )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired Access Token')
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail='Decode Erro')
    else:
        return decoded_jwt
    