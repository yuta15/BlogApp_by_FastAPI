from pydantic_settings import BaseSettings
import secrets
from datetime import timezone, timedelta


class SettingBase(BaseSettings):
    ALGORITHM: str = 'HS256'
    SECRET_KEY: str = secrets.token_hex()
    TZ: timezone = timezone(timedelta(hours=+9))
    
    
class DevSetting(SettingBase):
    DB_URL: str = 'sqlite:///test.db'
    ENV: str = 'Dev'
    EXPIRE_DELTA: timedelta = timedelta(minutes=15)
    