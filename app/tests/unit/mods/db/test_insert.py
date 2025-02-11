import pytest


from app.mods.db.insert import insert_data



def test_insert_user_data(db_session, create_users):
    """
    insert_data関数をテストするための関数
    """
    session = next(db_session)
    insert_users = create_users
    for user in insert_users:
        assert True == insert_data(session=session, data=user)
        


# def test_insert_article_data(db_session, create_articles):
#     """
#     insert_data関数のテスト。articleデータがinsert可能かをテストする。
#     """
#     session = next(db_session)
#     article = create_articles
    
        