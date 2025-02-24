from sqlmodel import select, Session
from sqlalchemy.exc import OperationalError, IntegrityError


def select_data(
    *,
    session: Session,
    stmts: list
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
        data = session.exec(statement=stmts).all()
    except (OperationalError, IntegrityError):
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    finally:
        return data
    