from sqlmodel import select, or_
from typing import List
from uuid import UUID
from pydantic import EmailStr

from app.deps.crud import SessionDeps
from app.models.User import User


def search_user(
    *, 
    session: SessionDeps,
    offset: int = 0,
    limit: int = 10,
    username: str | None=None,
    email: EmailStr | None =None,
    uuid: UUID | None =None,
    **kwargs
    ) -> List[User] | None:
    """
    ユーザー情報を検索するための関数
    """
    filters = []
    
    if username:
        filters.append(User.username.ilike(f'{username}'))
    if email:
        filters.append(User.email.ilike(f'{email}'))
    if uuid:
        filters.append(User.uuid.ilike(uuid))
    if kwargs:
        for key, val in kwargs.items():
            filters.append(User.username.ilike(f'{val}'))
            filters.append(User.email.ilike(f'{val}'))
            filters.append(User.email.uuid(f'{val}'))
    
    if offset == 0 and not filters:
        stmt = select(User).limit(limit=limit)
    elif not filters:
        stmt = select(User).offset(offset=offset).limit(limit=limit)
    elif offset == 0:
        stmt = select(User).where(or_(*filters)).limit(limit=limit)
    else:
        stmt = select(User).where(or_(*filters)).offset(offset=offset).limit(limit=limit)
    
    try:
        result = session.exec(stmt)
    except Exception as e:
        raise e
    else:
        return result