from datetime import datetime
from fastapi import Depends
from sqlmodel import Session, select
from typing import Annotated
from uuid import UUID, uuid4

from core.db import get_db
from core.security import create_password_hash
from core.setting import DevSetting
from models.db_models import User, UserOutput
from models.shemas import SchemaUserRegisterInput


SessionDeps  = Annotated[Session, Depends(get_db)]


def create_user(*, session: SessionDeps, user: SchemaUserRegisterInput):
    """
    ユーザー作成処理
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
    output_user = UserOutput.model_validate(insert_user)
    return output_user


def fetch_user_by_username(*, session: SessionDeps, username: str) -> UserOutput | None:
    """
    ユーザー名からユーザー情報を取得
    """
    stmt = select(User).where(User.username == username)
    user = session.exec(stmt).first()
    if user is None:
        return None
    user_output = UserOutput.model_validate(user)
    return user_output


def fetch_user_by_email(*, session: SessionDeps, email: str):
    """
    emailからユーザー情報を取得
    """
    stmt = select(User).where(User.email == email)
    user = session.exec(stmt).first()
    if user is None:
        return None
    user_output = UserOutput.model_validate(user)
    return user_output


def fetch_user_by_uuid(*, session: SessionDeps, uuid: UUID):
    """
    UUIDからユーザー情報を取得
    """
    stmt = select(User).where(User.uuid == uuid)
    user = session.exec(stmt).first()
    user_output = UserOutput.model_validate(user)
    return user_output
