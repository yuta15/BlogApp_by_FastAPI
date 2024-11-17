from passlib.context import CryptContext

from core.setting import DevSetting


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def create_password_hash(password: str):
    """
    パスワードをハッシュ化する関数
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    パスワード検証用関数
    """
    return pwd_context.verify(plain_password, hashed_password)