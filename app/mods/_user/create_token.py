from app.models.superuser.superuser import Superuser
from app.func.generate import generate_payload, generate_token


def create_token(
    user: Superuser
) -> str:
    """
    Tokenを作成するための関数。
    args: 
        user:User
            DBから取得したユーザー情報
    return: 
        token: str
            生成したToken情報
    """
    payload: dict = generate_payload.generate_payload(user_params=user)
    token: str = generate_token.generate_token(payload=payload)
    return token