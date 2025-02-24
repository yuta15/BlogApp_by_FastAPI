from sqlmodel import select, or_

from app.models.User import User
from app.mods.db.select import select_data




def search_user_by_conditions(*, session, method: bool=True, conditions:list=None):
    """
    特定の検索条件において検索する為の関数
    
    Args: 
        session: Session
            Required.DB Session
        method: bool = True
            True: and search
            False: or search
        conditions: list
            stmts list
    """
    query = select(User)
    if method:
        stmt = query.where(*conditions)
    else:
        stmt = query.where(or_(*conditions))
    datas = select_data(session=session, stmt=stmt)
    return datas
