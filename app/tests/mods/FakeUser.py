from uuid import uuid4
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from pydantic import EmailStr
from sqlmodel import select, delete
from typing import Any, Optional
import jwt
from sqlalchemy.exc import (
    DBAPIError, 
    DatabaseError, 
    IntegrityError, 
    InvalidRequestError,
    )

from app.tests.mods.get_db import get_db
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
        self.uuid = uuid4()
        self.username = user_params.get('username')
        self.password = user_params.get('password')
        self.email = user_params.get('email')
        self.tz = timezone(timedelta(hours=+9))
        self.create_at = self._time()
        self.update_at = self._time()
        self.token = None
        self.hashed_password = self._hasher(self.password)
        self.user = self._generate_db_mode()


    def _hasher(self, password) -> str:
        context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        return context.hash(password)


    def _time(self) -> datetime:
        return datetime.now(self.tz)
    
    
    def update_time(self) -> None:
        self.update_at = datetime.now(self.tz)
        self.user = self._generate_db_mode()


    def generate_token(self, payload, algorithm, secret_key) -> str:
        token: str = jwt.encode(
            payload=payload,
            key=secret_key,
            algorithm=algorithm
        )
        self.token = token


    def generate_payload(self, time_delta: timedelta, subject: dict):
        now = datetime.now(tz=self.tz)
        payload = {
            'iat': now,
            'exp': now + time_delta,
            'sub': subject
        }
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
                'is_active': False
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