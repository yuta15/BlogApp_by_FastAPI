import pytest
from sqlmodel import select

from app.mods.db.select import select_data
from app.models.User import User
from app.models.Article import Article



def test_select_user(db_session, create_users, insert_data_fixture):
    """select_dataのテスト"""
    user_count = 4
    session = db_session
    users = create_users(number = user_count)
    for user in users:
        insert_data_fixture(session, user)
        assert user == select_data(session=session, stmt=select(User).where(User.username == user.username))[0]
        assert user == select_data(session=session, stmt=select(User).where(User.email == user.email))[0]
        assert user == select_data(session=session, stmt=select(User).where(User.uuid == user.uuid))[0]


def test_select_articles(db_session, create_users, create_articles, insert_data_fixture):
    """select_dataのテスト"""
    user_count = 4
    session = db_session
    users = create_users(number=user_count)
    for user in users:
        insert_data_fixture(session=session, data=user)
        article = create_articles(user_id=user.uuid)[0]
        insert_data_fixture(session=session, data=article)
        assert article == select_data(session=session, stmt=select(Article).where(Article.id == article.id))[0]
