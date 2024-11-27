import os
from pydantic import EmailStr
from datetime import datetime


def generate_payload(username: str, email: EmailStr, iat, time_delta):
    """
    JWT用のPayloadを生成するための関数
    """
    payload = {
        'iat': iat,
        'exp': iat + time_delta,
        'sub':{
            'username': username,
            'email': email
        }
    }
    return payload