from sqlmodel import Session

from app.mods.db.generate_search_stmt import generate_search_stmt
from app.mods.db.select_data import select_data
from app.mods.db.parse_search_condition import parse_search_condition



def search(
    *,
    session:Session,
    model: any,
    search_conditions_list:list | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> list | None:
    """
    データを検索するための関数
    
    """
    is_and_condition = True
    if search_conditions_list:
        is_and_condition, search_conditions_list = parse_search_condition(search_conditions_list)
    stmt = generate_search_stmt(
        model=model, 
        is_and_condition=is_and_condition, 
        requirements=search_conditions_list, 
        offset=offset, 
        limit=limit
        )
    selected_data = select_data(session=session, stmt=stmt)
    return selected_data
    