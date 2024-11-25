from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlmodel import select, or_
from typing import Literal, List

from app.deps.crud import SessionDeps
from app.models.user.user_models import User
from app.models.superuser.superuser import Superuser


def fetch_users(
    *,
    session: SessionDeps,
    table_model: Literal[User, Superuser],
    condition: Literal['or', 'and'] = 'and',
    **kwargs: dict
) -> List[User | Superuser] | None:
    """
    一致するユーザー情報を取得するための関数
    
    args:
        session: SessionDeps
        table_model: Literal[User, Superuser]
            取得したテーブルごとに、User, Superuserを指定する。
            
        condition: Literal['or', 'and'] = 'and',
            kwargs内の情報をor検索もしくはand検索を指定する。
            デフォルトはand
        
        **kwargs: dict
            検索に必要な情報を指定する。
            可能な値は、username, email, uuidとなる。
            何も指定しない場合はすべてのユーザー情報を取得します。
            
    return:
        users: List[User | Superuser | None]
            table_modelでUserを指定した場合はUserモデルに従いリターンする。
            Superuserを指定した場合は、Superuserモデルに従いリターンする。
            ヒットした情報がない場合は、[]がリターンされる。
    
    Exception:
        何らかの影響でサーバーから正常に応答がない場合は、HTTP_500_INTERNAL_SERVER_ERRORを返す。
    """
    
    filters = []
    for column, field in kwargs.items():
        if column == 'uuid':
            filters.append(table_model.uuid == field)
        elif column == 'username':
            filters.append(table_model.username == field)
        elif column == 'email':
            filters.append(table_model.email == field)
    
    if not filters:
        stmt = select(table_model)
    
    if condition == 'or':
        stmt = select(table_model).where(or_(*filters))
    else:
        stmt = select(table_model).where(*filters)
    
    try:
        users: List[User | Superuser | None] = session.exec(stmt).all()
    except:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Internal Server Error. Please try again later.'
        )
    else:
        if not users:
            return None
        return users