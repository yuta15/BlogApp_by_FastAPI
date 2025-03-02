import pytest

from app.mods.db.delete_data import delete_data

def test_delete_user(db_session, create_users, insert_data_fixture):
    """
    ユーザー削除機能のテスト
    """
    session = db_session
    user_count = 4
    users = create_users(
        number = user_count,
    )
    for user in users:
        insert_data_fixture(session=session, data=user)
    
    for user in users:
        assert True == delete_data(session=session, data=user)


def test_delete_articles(db_session, create_users, insert_data_fixture, create_articles):
    """
    Article削除機能のテスト
    """
    session = db_session
    user_count = 4
    only_user_article_count = 4
    articles = []
    users = create_users(
        number = user_count,
        is_only_normal_user=True,
        is_only_active_user=True
    )
    for user in users:
        articles = articles + create_articles(user_id=user.uuid, number=only_user_article_count)
        insert_data_fixture(session=session, data=user)

    for article in articles:
        insert_data_fixture(session=session, data=article)
    
    for article in articles:
        assert True == delete_data(session=session, data=article)
