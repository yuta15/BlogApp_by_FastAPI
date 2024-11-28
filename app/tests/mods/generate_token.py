import os
import jwt

from app.tests.mods.generate_payload import generate_payload


def generate_token(payload: dict, secret_key='dev-secret-key'):
    """
    JWTを生成するためのモジュール
    """
    algorithm = os.environ.get('ALGORITHM')
    token: str = jwt.encode(
        payload=payload,
        key=secret_key,
        algorithm=algorithm
        )
    return token

