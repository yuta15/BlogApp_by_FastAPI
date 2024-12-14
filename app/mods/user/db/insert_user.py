from fastapi import HTTPException
from sqlalchemy.exc import OperationalError, InterfaceError, DBAPIError, TimeoutError, IntegrityError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.deps.crud import SessionDeps
from app.models.User import User


def insert_user(
    *,
    session: SessionDeps,
    user: User
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
    except OperationalError:
        session.rollback()
        return False
    except InterfaceError:
        session.rollback()
        return False
    except TimeoutError:
        session.rollback()
        return False
    except IntegrityError:
        session.rollback()
        return False
    except DBAPIError:
        session.rollback()
        return False
    except Exception:
        session.rollback()
        return False
    else:
        return True