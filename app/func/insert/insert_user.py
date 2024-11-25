from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.deps.crud import SessionDeps
from app.models.user.user_models import User
from app.models.superuser.superuser import Superuser


def insert_user(
    *,
    session: SessionDeps,
    user: User | Superuser,
) -> None:
    """
    args:
        session: SessionDeps,
        user: User | Superuser,
            テーブルに入力するデータ
    return:
        None
    Exception:
        HTTP_500_INTERNAL_SERVER_ERROR
    """
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Internal Server Error. Please try again later.'
            )