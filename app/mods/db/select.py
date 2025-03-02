from sqlmodel import Session

from app.mods.db.generate_select_stmt import generate_select_stmt
from app.mods.db.select_data import select_data

def begin_select(
    *,
    session:Session,
    model: any,
    is_and_condition: bool=True,
    search_requirements:list,
    offset: int | None = None,
    limit: int | None = None,
) -> list | None:
    """
    
    
    """
    if search_requirements:
        search_requirements = parse_validate_search_requirements(search_requirements)
    stmt = generate_select_stmt(
        model=model, 
        is_and_condition=is_and_condition, 
        requirements=search_requirements, 
        offset=offset, 
        limit=limit
        )
    selected_data = select_data(session=session, stmt=stmt)
    return selected_data
    