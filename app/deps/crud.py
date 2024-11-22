from datetime import datetime
from fastapi import Depends
from sqlmodel import Session, select, or_
from typing import Annotated, List, Literal, Optional
from pydantic import EmailStr
from uuid import UUID, uuid4

from core.db import get_db
from core.security import create_password_hash
from core.setting import DevSetting
from models.user_models import User, UserOutput
from models.user_models import SchemaUserRegisterInput


SessionDeps  = Annotated[Session, Depends(get_db)]


def create_user(*, session: SessionDeps, user: SchemaUserRegisterInput):
    """
    ユーザー作成
    """
    now = datetime.now(tz=DevSetting().TZ)
    insert_user = User.model_validate(user, update={
        'uuid':uuid4(),
        'create_at': now,
        'update_at': now,
        'hashed_password': create_password_hash(user.plain_password)
    })
    session.add(insert_user)
    session.commit()
    session.refresh(insert_user)
    return insert_user


def fetch_users(
    *, 
    session: SessionDeps, 
    uuid: UUID = None, 
    username: str = None, 
    email: EmailStr = None,
    condition: Optional[Literal['or', 'and']] = 'and',
    ):
    """
    条件に合致するユーザーの情報を取得する関数。
    args:
        session: SessionDeps
        uuid: UUID | None
        username: str | None
        email: EmailStr | None
        condition: Optional[Literal['or', 'and']], default='and'
    return:
        Users: List[User]
    """
    filters = []
    if uuid is not None:
        filters.append(User.uuid == uuid)
    if username is not None:
        filters.append(User.username == username)
    if email is not None:
        filters.append(User.email == email)
    
    if condition == 'and':
        stmt = select(User).where(*filters)
    elif condition == 'or':
        stmt = select(User).where(or_(*filters)) 
        
    users: List[User] = session.exec(stmt).all()
    
    return users