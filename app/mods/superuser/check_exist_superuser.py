from typing import List
from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT


from app.deps.crud import SessionDeps
from app.models.superuser.superuser import Superuser, SuperuserInput
from app.func.fetch.fetch_users import fetch_users


def check_exist_user(
    *,
    session: SessionDeps,
    user_input: SuperuserInput
    ) -> bool:
    """
    DB内の情報を確認し、ユーザー名、emailが重複しないことを確認する。
    args: 
        session: SessionDeps
        user_input: UserModel
        
    return:
        bool
    
    Exception:

    """
    users: List[Superuser] = fetch_users(
        session=session,
        table_model=Superuser,
        condition='or',
        username=user_input.username.encode('utf-8'),
        email=user_input.email.encode('utf-8')
    )
    
    if users:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, 
            detail='Input username or email is confilict'
            )