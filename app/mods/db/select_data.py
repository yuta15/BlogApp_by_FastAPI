from sqlmodel import Session
from sqlalchemy.exc import OperationalError, IntegrityError


def select_data(
    *,
    session: Session,
    stmt: any
) -> list:
    """
    DBからデータを取得するための関数
    
    session: 
        セッション
    stmts:List
        statementのリスト
        
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
    