from sqlmodel import select, or_
from app.models.User import User
from typing import List
from sqlalchemy.exc import OperationalError, TimeoutError, DBAPIError

def fetch_users(*,session,**kwargs):
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
        return False
    stmt = select(User).where(or_(**filters))
    
    try:
        users: List[User|  None] = session.exec(stmt).all()
    except OperationalError as e:
        raise OperationalError(f'{e}: Can not fetch user data')
    except DBAPIError as e:
        raise DBAPIError(f'{e}: Can not fetch user data')
    except TimeoutError as e:
        raise DBAPIError(f'{e}: Can not fetch user data')
    else:
        return users