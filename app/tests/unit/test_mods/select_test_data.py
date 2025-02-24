from sqlmodel import Session
from sqlalchemy.exc import OperationalError, IntegrityError


def select_test_data(
    *,
    session: Session,
    stmt: any
) -> list:
    """
    DBからデータを取得するための関数
    Args:
        session: 
            セッション
        stmt:any
            statement
    retun:
        list[data]
    """
    try:
        data = session.exec(statement=stmt).all()
    except (OperationalError, IntegrityError):
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    finally:
        return data
    