from fastapi import HTTPException
from sqlalchemy.exc import OperationalError, InterfaceError, DBAPIError, TimeoutError, IntegrityError
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
    except OperationalError as e:
        session.rollback()
        return {
            'Error': 'OperationalError',
            'result': f'{e}'
            }
    except InterfaceError as e:
        session.rollback()
        return {
            'Error': 'InterfaceError',
            'result': f'{e}'
        }
    except TimeoutError as e:
        session.rollback()
        return {
            'Error': 'TimeoutError',
            'result': f'{e}'
        }
    except IntegrityError as e:
        session.rollback()
        return {
            'Error': 'IntegrityError',
            'result': f'{e}'
        }
    except DBAPIError as e:
        session.rollback()
        return {
            'Error': 'DBAPIError',
            'result': f'{e}'
        }
    except Exception as e:
        session.rollback()
        return {'result': f'{e}'}