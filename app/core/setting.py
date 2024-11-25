from pydantic_settings import BaseSettings
import secrets
from datetime import timezone, timedelta
from passlib.context import CryptContext


class Setting(BaseSettings):
    ENV: str
    ALGORITHM: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOSTNAME: str
    DB_PORT: str
    DB_NAME:str
    SECRET_KEY: str = secrets.token_hex()
    TZ: timezone = timezone(timedelta(hours=+9))
    EXPIRE_DELTA: timedelta = timedelta(minutes=15)
    
    @property
    def DB_URL(self) -> str:
        return f'mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOSTNAME}:{self.DB_PORT}/{self.DB_NAME}'


setting = Setting()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
