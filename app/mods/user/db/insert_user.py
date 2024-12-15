from fastapi import HTTPException
from sqlalchemy.exc import OperationalError, InterfaceError, DBAPIError, TimeoutError, IntegrityError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.deps.crud import SessionDeps
from app.models.User import User


def insert_user(
    *,
    session: SessionDeps,
    user_params: User
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
        session.add(user_params)
        session.commit()
        session.refresh(user_params)
    except (
        OperationalError,
        InterfaceError,
        TimeoutError,
        IntegrityError,
        DBAPIError,
        Exception
        ) as e:
        session.rollback()
        raise e
    else:
        return True