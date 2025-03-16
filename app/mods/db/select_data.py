from sqlalchemy.exc import OperationalError, IntegrityError

from app.deps.crud import SessionDeps
    

def select_data(
    *,
    session: SessionDeps,
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
        raise
    except Exception:
        raise
    else:
        return data
    