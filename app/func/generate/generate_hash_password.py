from app.core.setting import pwd_context


def generate_hash_password(plain_password: str) -> str:
    """
    ハッシュ化したパスワードを生成するための関数。
    args:
        plain_password: str
        プレーンテキストパスワード
    return:
        hashed_password: str
        ハッシュ化したパスワード
    """
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password