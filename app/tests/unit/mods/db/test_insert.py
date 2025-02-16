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


def test_insert_article_data(db_session, create_users, create_articles, insert_data_fixture):
    """
    articleテストの改良版
    """
    dict_users = []
    articles = []
    users = create_users(
        number=4,
        is_only_normal_user=True,
        is_only_active_user=True
    )
    session = db_session
    for user in users:
        user_id = user.uuid
        dict_users.append(dict(user))
        insert_data_fixture(user)
        only_user_article = create_articles(user_id=user_id, number=3)
        articles = articles + only_user_article

    for article in articles:
        assert True == insert_data(session=session, data=article)