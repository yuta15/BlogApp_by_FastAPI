from datetime import datetime
from sqlmodel import select
from typing import List
import jwt

from app.core.db import get_db
from app.core.security import setting
from app.models.user.user_models import User


def generate_tokens(users: List[User]) -> List[str]:
    """
    Token生成用関数
    """
    tokens = []
    for user in users:
        token = jwt.encode(
            payload={
                'iat': datetime.now(setting.TZ),
                'exp': datetime.now(setting.TZ) + setting.EXPIRE_DELTA,
                'sub': {
                    'username': user.username,
                    'email': user.email,
                }
            }
        )
        tokens.append(token)
    return tokens


def get_all_user() -> List[User]:
    """
    すべてのユーザー情報を取得する
    """
    session = get_db()
    stmt = select(User)
    users = session.exec(stmt).all()
    return users


def create_token_headers() -> List[dict]:
    users: List[User] = get_all_user()
    tokens: List[str] = generate_tokens(users=users)
    headers = []
    for token in tokens:
        header = {"Authorization": f"Bearer {token}"}
        headers.append(header)
    return headers
    
