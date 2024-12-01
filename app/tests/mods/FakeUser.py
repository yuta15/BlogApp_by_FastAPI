from uuid import uuid4, UUID
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from pydantic import EmailStr
import jwt
from sqlalchemy.exc import (
    DBAPIError, 
    DatabaseError, 
    IntegrityError, 
    InvalidRequestError,
    )

from app.core.setting import setting
from app.models.user.user_models import User

class FakeUser:
    """
    テストデータを生成するためのクラス
    
    """
    
    def __init__(
        self, 
        user_params: dict,
    ) -> None:
        """
        user_paramsにはusername, password, emailが必須です。
        args:
            user_params:
                username: str
                password: str
                email: EmailStr
        """
        self.uuid: UUID = uuid4()
        self.username: str = user_params.get('username')
        self.password: str = user_params.get('password')
        self.email: EmailStr = user_params.get('email')
        self.tz: timezone = timezone(timedelta(hours=+9))
        self.create_at: datetime = self._time()
        self.update_at: datetime = self._time()
        self.payload: dict = None
        self.token: str = None
        self.hashed_password: str = self._hasher(self.password)
        self.user: User = self._generate_db_mode()


    def _hasher(self, password) -> str:
        context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        return context.hash(password)


    def _time(self) -> datetime:
        return datetime.now(self.tz)
    
    
    def update_time(self) -> None:
        self.update_at = datetime.now(self.tz)
        self.user = self._generate_db_mode()


    def generate_token(self, **kwargs) -> str:
        """
        tokenを生成する。
        生成されたTokenはオブジェクトにも設定される。
        
        kwargs parameters:
            payload: object [require]
            key: secret_key [Default: setting.SECRET_KEY]
            algorithm: [str] [Default: setting.ALGORITHM]
        """
        token: str = jwt.encode(
            payload = kwargs.get('payload'),
            key = kwargs.get('secret_key', setting.SECRET_KEY),
            algorithm = kwargs.get('algorithm', setting.ALGORITHM)
        )
        self.token = token
        return token


    def generate_payload(self, **kwargs) -> dict:
        """
        iat, exp, subject情報をkwargsに含めることができる。
        
        kwargs parameters:
            iat: datetime [Default: datetime.now(tz=self.tz)]
            time_delta: timedelta [require]
            subject: dict
        """
        iat: datetime = kwargs.get('iat', datetime.now(tz=self.tz))
        exp: datetime = iat + kwargs.get('time_delta')
        subject: dict = kwargs.get('subject')
        payload = {
            'iat': iat,
            'exp': exp,
            'sub': subject
        }
        self.payload = payload
        return payload


    def _generate_db_mode(self):
        """
        Insert用のデータを生成
        """
        user = User.model_validate(
            {
                'uuid': self.uuid,
                'username': self.username,
                'email': self.email,
                'create_at': self.create_at,
                'update_at': self.update_at,
                'hashed_password': self.hashed_password,
                'is_active': True
            }
        )
        return user
    
    
    def insert_user(self, session):
        """
        データをDBにinsertする関数
        """
        try:
            session.add(self.user)
            session.commit()
            session.refresh(self.user)
        except (
            DBAPIError, 
            DatabaseError, 
            IntegrityError, 
            InvalidRequestError,
            
        ) as e:
            raise e


    def delete_user(self, session):
        """
        データを削除する。
        """
        try:
            session.delete(self.user)
            session.commit()
            session.close()
        except (
            DBAPIError, 
            DatabaseError, 
            IntegrityError, 
            InvalidRequestError,
        ) as e:
            raise e