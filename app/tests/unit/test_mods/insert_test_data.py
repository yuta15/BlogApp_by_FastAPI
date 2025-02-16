


def insert_test_data(
    session,
    data
):
    """
    test用のdataをinsertする為の関数
    """
    try:
        session.add(data)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return True