from sqlmodel import select, Session, or_
from sqlalchemy.exc import OperationalError, DataError, ProgrammingError, InvalidRequestError, TimeoutError
from typing import Literal, List

from app.models.user.user_models import User


def fetch_user(
    *,
    session: Session,
    condition: Literal['or', 'and'] = 'and',
    **kwargs: dict
)->User:
    """
    args
        session:
            DBセッション
        condition: str,
            'and', 'or'を入力
        **kwargs
            username, uuid, emailを指定可能。
    return
        User
    """
    filters = []
    for column, field in kwargs.items():
        if column == 'uuid':
            filters.append(User.uuid == field)
        elif column == 'username':
            filters.append(User.username == field)
        elif column == 'email':
            filters.append(User.email == field)
    
    if not filters:
        stmt = select(User)
    
    if condition == 'or':
        stmt = select(User).where(or_(*filters))
    else:
        stmt = select(User).where(*filters)
    
    try:
        users: List[User | None] = session.exec(stmt).all()
    except (OperationalError, DataError, ProgrammingError, InvalidRequestError, TimeoutError) as e:
        raise e(f'Error')
    else:
        return users