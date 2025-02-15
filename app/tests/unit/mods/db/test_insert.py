import pytest


from app.mods.db.insert import insert_data



def test_insert_user_data(db_session, create_users):
    """
    insert_data関数をテストするための関数
    """
    insert_users = create_users(number=4)
    session = db_session
    for user in insert_users:
        assert True == insert_data(session=session, data=user)


def test_insert_article_data(db_session, inserted_user, create_articles):
    """
    insert_data関数のテスト。articleデータがinsert可能かをテストする。
    """
    user = inserted_user
    articles = create_articles(user_id=user['uuid'])
    session = db_session
    for article in articles:
        assert True == insert_data(session=session, data=article)


