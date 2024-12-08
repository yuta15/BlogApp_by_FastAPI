from uuid import uuid4, UUID
from sqlmodel import select
from datetime import datetime, timezone, timedelta
from pydantic import EmailStr
import jwt
from sqlalchemy.exc import OperationalError, InterfaceError, DBAPIError
from sqlalchemy.exc import (
    DBAPIError, 
    DatabaseError, 
    IntegrityError, 
    InvalidRequestError,
    )

from app.core.setting import setting, pwd_context
from app.models.User import User, UserRegister


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
        self.hashed_password: str = pwd_context.hash(self.password)
        self.user: User = self._generate_db_model()
        self.input_user: UserRegister = self._generate_input_model()
        
    def verify_hash(self, plain_password, hash_password):
        return pwd_context.verify(secret=plain_password, hash=hash_password)


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
    
    
    def _generate_input_model(self):
        """
        ユーザーから受信するデータ
        """
        input_user = UserRegister.model_validate(
            {
                'username': self.username,
                'email': self.email,
                'password': self.password
            }
        )
        return input_user


    def _generate_db_model(self):
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
        
        
    def fetch_user_by_username(self, session):
        """
        ユーザー名からデータを取得するための関数
        """
        try:
            stmt = select(self.user).where(username=self.username)
            session.exec(stmt).all()
        except (OperationalError, DBAPIError, InterfaceError) as e:
            raise e(f'{e}: In FakeUser class')