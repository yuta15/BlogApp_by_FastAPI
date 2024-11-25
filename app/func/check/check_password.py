from app.core.setting import pwd_context

def check_password(
    plain_password: str,
    hashed_password: str
    ) -> bool:
    """
    受信したパスワードの検証を実施する。
    args:
        plain_password: str,
        hashed_password: str
    return:
        is_valid: bool
    """
    is_valid = pwd_context.verify(plain_password, hashed_password)
    return is_valid