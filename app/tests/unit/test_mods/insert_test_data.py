
from app.core.db import get_db


def insert_test_data(
    data
):
    """
    test用のdataをinsertする為の関数
    """
    session = next(get_db())
    try:
        session.add(data)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    return True