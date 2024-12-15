from sqlmodel import select, or_
from app.models.User import User
from typing import List
from sqlalchemy.exc import OperationalError, TimeoutError, DBAPIError

def fetch_users(*,session,**kwargs) -> object:
    """
    UUID、ユーザー名、Emailの値から一意のユーザーを取得するための関数です。
    **kwargsにはuuid, username, emailを含めることができます。
    それ以外の値を指定した場合は考慮されません。
    kwargsを指定しない場合、すべてのユーザー情報が取得されます。
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
    else:
        stmt = select(User).where(or_(*filters))
    
    try:
        users: List[User] = session.exec(stmt)
    except (OperationalError, DBAPIError, TimeoutError) as e:
        raise e
    else:
        return users