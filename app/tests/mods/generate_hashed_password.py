from passlib.context import CryptContext


def generate_hashed_password(password: str):
    """
    hash化したパスワードを生成する。
    """
    pwd_cotext = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_password = pwd_cotext.hash(password)
    return hashed_password